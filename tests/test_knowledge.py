"""The reference lookup: parsing the knowledge files, ranking, trimming and caching."""

from __future__ import annotations

import os
import re
import threading

import pytest

from kenshi_link import knowledge
from kenshi_link.knowledge import UNVERIFIED_NOTE, KnowledgeBase, stem

TOWNS = """\
# Towns and traders

Where the towns are and what their shops buy and sell.

## The Hub (town)
Also: starting town, ruined town, Border Zone bar
- The Hub is a ruined town in the middle of the Border Zone.
- The bar sells food and buys almost anything, including copper ore.
- Copper and iron nodes lie just outside the walls.

## Squin (town)
Also: Shek town
- Squin is a Shek Kingdom town south-west of The Hub.
- Its shops pay full price for armour. (unverified)

## Selling items to a trader
Also: vendor, shop, merchant, trade goods
- Talk to the trader, then drag items from your inventory into theirs.
- Traders run out of money; each shop restocks about once a day.

## Sources
- https://kenshi.fandom.com/wiki/The_Hub - location and shops of the Hub and Squin.
- https://kenshi.fandom.com/wiki/Trading - how selling to a vendor works.
"""

MEDICAL = """\
# Medical

How wounds, bleeding and recovery work.

## Bleeding and bandaging
Also: blood loss, first aid, medkit
- A cut makes a character bleed; blood loss leads to unconsciousness and then death.
- Use a First Aid Kit on the wounded body part to bandage it.

## Beds and resting
Also: sleep, heal faster
- Beds heal much faster than standing around.
- Bars rent beds for a few cats, and a rested character stops bleeding sooner.

## Bonedogs
- A Bonedog is a fast wild dog that hunts in packs.
"""

CONTROLS = """\
# Controls

What the buttons on the screen do.

## Hold button
Also: hold position, stay put
- With Hold on, the selected characters stay where they are and do not chase enemies.

## Passive button
- With Passive on, characters do not attack.
"""


def write(directory, name: str, text: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_bytes(text.encode("utf-8"))


def shown(text: str) -> list[str]:
    """The labels of the sections a search returned, in order."""
    return [line[3:] for line in text.splitlines() if line.startswith("## ")]


@pytest.fixture
def base(tmp_path) -> KnowledgeBase:
    directory = tmp_path / "knowledge"
    write(directory, "towns.md", TOWNS)
    write(directory, "medical.md", MEDICAL)
    write(directory, "controls.md", CONTROLS)
    return KnowledgeBase(directory)


def one_file(tmp_path, text: str, name: str = "notes.md") -> KnowledgeBase:
    write(tmp_path / "kb", name, text)
    return KnowledgeBase(tmp_path / "kb")


# ---- parsing -------------------------------------------------------------------


def test_files_split_into_labelled_sections(base):
    sections = base.sections
    assert [section.heading for section in sections if section.source == "towns.md"] == [
        "The Hub (town)",
        "Squin (town)",
        "Selling items to a trader",
    ]
    hub = next(section for section in sections if section.heading == "The Hub (town)")
    assert hub.title == "Towns and traders" and hub.label == "Towns and traders > The Hub (town)"
    assert hub.also == "starting town, ruined town, Border Zone bar"
    assert hub.body.startswith("- The Hub is a ruined town") and "Also:" not in hub.body
    assert len(sections) == 8


def test_sources_sections_are_not_searchable(base):
    assert all("Sources" not in section.heading for section in base.sections)
    assert "fandom" not in " ".join(section.body for section in base.sections)
    assert "Sources" not in base.topics()
    assert shown(base.search("fandom wiki")) == []


def test_a_differently_named_list_of_links_is_skipped_but_a_real_section_is_not(tmp_path):
    kb = one_file(
        tmp_path,
        "# Food\n\nWhat to eat.\n\n"
        "## Sources of food\n- Bars sell dried meat.\n- Farms grow wheat.\n\n"
        "## Sources and what they supported\n- https://example.org/a - prices\n- https://example.org/b - farms\n",
    )
    assert [section.heading for section in kb.sections] == ["Sources of food"]


# ---- ranking -------------------------------------------------------------------


def test_the_section_that_answers_comes_first(base):
    assert shown(base.search("stop bleeding"))[0] == "Medical > Bleeding and bandaging"
    assert shown(base.search("what does the Hold button do"))[0] == "Controls > Hold button"
    result = base.search("where to sell copper ore near the Hub")
    assert shown(result)[0] == "Towns and traders > The Hub (town)"
    assert "- The bar sells food and buys almost anything, including copper ore." in result


def test_a_second_section_named_for_another_query_word_is_kept(base):
    # The Hub section wins on most words; the selling section is the one named for "sell".
    assert shown(base.search("where to sell copper ore near the Hub"))[:2] == [
        "Towns and traders > The Hub (town)",
        "Towns and traders > Selling items to a trader",
    ]


def test_heading_and_also_matches_outrank_body_matches(tmp_path):
    kb = one_file(
        tmp_path,
        "# Weights\n\nOne word in three places.\n\n"
        "## In the body\n- Lockpicks open doors. Lockpicks break. Carry spare lockpicks.\n\n"
        "## In the also line\nAlso: lockpicks\n- Tools for doors.\n\n"
        "## Lockpicks\n- Tools for doors.\n\n"
        "## Unrelated\n- Nothing to see here.\n",
    )
    ranked = [match.section.heading for match in kb.rank("lockpicks")]
    assert ranked == ["Lockpicks", "In the also line", "In the body"]
    scores = [match.score for match in kb.rank("lockpicks")]
    assert scores[0] > scores[1] > 2 * scores[2]


def test_a_word_in_the_heading_settles_what_a_section_is_about(tmp_path):
    kb = one_file(
        tmp_path,
        "# Places\n\nTowns and what is near them.\n\n"
        "## Mining\nAlso: copper near the Hub, Hub ore\n"
        "- The Hub has ore. Dig north of the Hub, or west of the Hub. The Hub buys it.\n\n"
        "## Where to mine copper, iron and stone around the Hub\n- Bring a backpack.\n\n"
        "## The Hub (town)\n- A ruined town in the Border Zone.\n\n"
        "## Squin (town)\n- A Shek town.\n\n"
        "## The Hub: bar, selling and buying\n- Open day and night.\n\n"
        "## Bars\nAlso: Hub bar\n- A bar sells food. Every bar rents beds. The Hub has a bar.\n",
    )
    # The name alone: the section named for it and little else, however often others repeat it.
    ranked = [match.section.heading for match in kb.rank("the hub")]
    assert ranked[0] == "The Hub (town)" and "Squin (town)" not in ranked
    assert sorted(ranked[1:]) == [
        "Bars",
        "Mining",
        "The Hub: bar, selling and buying",
        "Where to mine copper, iron and stone around the Hub",
    ]
    # A heading that holds every query word comes before headings that hold some of them.
    assert kb.rank("which town is the Hub")[0].section.heading == "The Hub (town)"


def test_a_word_in_the_file_title_helps_a_little(tmp_path):
    directory = tmp_path / "kb"
    write(directory, "a.md", "# Regions\n\nPlaces.\n\n## Venge\n- Beams burn by day.\n\n## Shem\n- Few hazards.\n")
    write(directory, "b.md", "# Hazards\n\nDangers.\n\n## Beams\n- They burn by day.\n\n## Acid\n- Wear a hat.\n")
    kb = KnowledgeBase(directory)
    # Between two sections that say the same, the one in the file about hazards comes first.
    assert [match.section.heading for match in kb.rank("burn hazards")][:2] == ["Beams", "Venge"]
    # But a section that mentions the word beats those that only sit in a file titled with it.
    ranked = kb.rank("hazards")
    assert [match.section.heading for match in ranked] == ["Shem", "Beams", "Acid"]
    assert ranked[0].score > 2 * ranked[1].score
    assert shown(kb.search("hazards")) == ["Regions > Shem"]


def test_sections_far_behind_the_best_are_named_but_not_shown(base, tmp_path):
    assert base.search("what does the Hold button do") == (
        "## Controls > Hold button\n"
        "- With Hold on, the selected characters stay where they are and do not chase enemies."
    )
    kb = one_file(
        tmp_path,
        "# Blades\n\nSwords.\n\n"
        "## Katanas\n- Fast, light blades.\n\n"
        "## Where the Shek smiths sell their finest blades\nAlso: katana\n- In Squin.\n\n"
        "## Sheaths\n- Worn on the hip or the back, where a katana can also go.\n\n"
        "## Other things entirely\n- Nothing.\n",
    )
    first, second, third = kb.rank("katana")
    assert 0.25 * first.score <= second.score < 0.5 * first.score and third.score < 0.25 * first.score
    assert kb.search("katana") == (
        "## Blades > Katanas\n- Fast, light blades.\n\n"
        "Also relevant, not shown: Blades > Where the Shek smiths sell their finest blades."
    )


def test_also_line_finds_a_section_by_a_synonym(base):
    assert shown(base.search("medkit")) == ["Medical > Bleeding and bandaging"]
    assert shown(base.search("vendor"))[0] == "Towns and traders > Selling items to a trader"
    assert "Also:" not in base.search("vendor")


def test_matching_more_distinct_terms_beats_repeating_one(tmp_path):
    kb = one_file(
        tmp_path,
        "# Metals\n\nWhere to dig.\n\n"
        "## Repeats\n- Copper here. Copper there. Copper everywhere. More copper. Copper again.\n\n"
        "## Covers\n- There is copper ore near the Hub.\n\n"
        "## Filler\n- Sand and wind.\n",
    )
    assert [match.section.heading for match in kb.rank("copper ore hub")] == ["Covers", "Repeats"]


@pytest.mark.parametrize(
    "query, expected",
    [
        ("BLEEDING!!!", "Medical > Bleeding and bandaging"),
        ("my character bled", "Medical > Bleeding and bandaging"),
        ("bandages", "Medical > Bleeding and bandaging"),
        ("bandaged?", "Medical > Bleeding and bandaging"),
        ("first-aid kits", "Medical > Bleeding and bandaging"),
        ("the hub's bar", "Towns and traders > The Hub (town)"),
        ("towns that are ruined", "Towns and traders > The Hub (town)"),
        ("sold an item to traders", "Towns and traders > Selling items to a trader"),
        ("holding position", "Controls > Hold button"),
        ("bone dog", "Medical > Bonedogs"),
        ("bonedog", "Medical > Bonedogs"),
        ("armor prices", "Towns and traders > Squin (town)"),
    ],
)
def test_inflection_case_and_punctuation_do_not_matter(base, query, expected):
    assert shown(base.search(query))[0] == expected


def test_stemming_joins_inflected_forms_and_keeps_different_words_apart():
    for family in (
        "mine mines mined mining",
        "sell sells selling sold",
        "bandage bandages bandaged bandaging",
        "body bodies",
        "carry carries carried carrying",
        "stop stops stopped stopping",
        "die dies died dying dead",
        "armour armor armoured armours",
        "thief thieves",
    ):
        assert len({stem(word) for word in family.split()}) == 1, family
    assert len({stem(word) for word in "hub hunger thing king bed bus copper forest".split()}) == 8
    assert stem("thing") == "thing" and stem("bus") == "bus" and stem("forest") == "forest"


def test_a_related_word_form_matches_at_a_discount(tmp_path):
    kb = one_file(
        tmp_path,
        "# Jobs\n\nWho does what.\n\n"
        "## Traders\n- They buy and sell.\n\n"
        "## Trade\n- Moving goods between towns.\n\n"
        "## Storage\n- Boxes and barrels.\n\n"
        "## Storm\n- Bad weather can drag on.\n",
    )
    assert [match.section.heading for match in kb.rank("trade")] == ["Trade", "Traders"]
    assert [match.section.heading for match in kb.rank("safest store")] == ["Storage"]
    assert kb.rank("dragon") == []  # not a form of "drag", as "store" is not of "storm"


# ---- trimming ------------------------------------------------------------------


def test_limit_caps_the_number_of_sections(base):
    assert len(shown(base.search("town", limit=1))) == 1
    assert len(shown(base.search("town", limit=2))) == 2
    assert "Also relevant, not shown: " in base.search("town", limit=1)


def test_budget_trims_at_section_boundaries(base):
    full = base.search("town bar shop")
    labels = shown(full)
    assert len(labels) >= 3
    texts = {section.label: section.text for section in base.sections}
    assert len(base.search("town bar shop", max_chars=len(full))) == len(full)
    for budget in (len(full) - 1, 450, 300):
        trimmed = base.search("town bar shop", max_chars=budget)
        assert len(trimmed) <= budget
        kept = shown(trimmed)
        assert kept and kept[0] == labels[0] and len(kept) < len(labels)
        for label in kept:  # every section that is there is there whole
            assert texts[label] in trimmed
    dropped = base.search("town bar shop", max_chars=len(full) - 1)
    assert shown(dropped) == labels[:2]
    assert f"Also relevant, not shown: {labels[2]}." in dropped


def test_a_section_larger_than_the_budget_is_cut_at_a_line_break(tmp_path):
    bullets = "".join(f"- Fact number {i} about the long topic, with some padding words.\n" for i in range(40))
    kb = one_file(tmp_path, f"# Long\n\nOne long section.\n\n## Long topic\n{bullets}")
    result = kb.search("long topic", max_chars=500)
    assert len(result) <= 500
    lines = result.splitlines()
    assert lines[0] == "## Long > Long topic" and lines[-1] == "[Section cut here to fit the length limit.]"
    assert all(line.endswith("padding words.") for line in lines[1:-1]) and len(lines) > 4


def test_the_best_section_is_cut_rather_than_passed_over(tmp_path):
    bullets = "".join(f"- Katana fact {i}, padded out to the length of a real bullet point.\n" for i in range(30))
    kb = one_file(
        tmp_path,
        f"# Weapons\n\nBlades.\n\n## Katanas\n{bullets}\n## Katana shops\n- Sold in Squin. (unverified)\n",
    )
    assert shown(kb.search("katanas")) == ["Weapons > Katanas", "Weapons > Katana shops"]
    result = kb.search("katanas", max_chars=600)
    assert len(result) <= 600 and shown(result) == ["Weapons > Katanas"]
    assert "[Section cut here to fit the length limit.]\n\nAlso relevant, not shown: Weapons > Katana shops." in result
    assert "unverified" not in result


def test_tiny_budgets_still_return_something(base):
    result = base.search("bleeding", max_chars=0)
    assert shown(result) == ["Medical > Bleeding and bandaging"] and len(result) <= 300


# ---- no match ------------------------------------------------------------------


def test_nothing_matching_says_so_and_returns_no_sections(base):
    result = base.search("tame a dragon")
    assert result.startswith('Nothing in the Kenshi reference matches "tame a dragon".')
    assert "No section mentions: tame, dragon." in result
    assert shown(result) == [] and "\n- " not in result


def test_a_weak_match_offers_headings_instead_of_text(base):
    # "rent" is in one body and "dragon" is nowhere: not enough to call an answer.
    result = base.search("dragon rent")
    assert result.startswith('No section of the Kenshi reference matches "dragon rent" well.')
    assert "Closest headings:\n- Medical > Beds and resting" in result
    assert "No section mentions: dragon." in result
    assert shown(result) == [] and "Beds heal much faster" not in result


def test_a_misspelled_name_offers_the_heading_it_resembles(base):
    result = base.search("Skuin")
    assert "Closest headings:\n- Towns and traders > Squin (town)" in result
    assert "No section mentions: skuin." in result and shown(result) == []


def test_a_missing_word_is_reported_beside_a_good_match(base):
    result = base.search("dragon bleeding")
    assert shown(result)[0] == "Medical > Bleeding and bandaging"
    assert "No section mentions: dragon." in result


@pytest.mark.parametrize("query", ["", "   ", "?!", None, "what should I do", "how is it"])
def test_a_query_without_searchable_words_is_answered_without_searching(base, query):
    assert base.search(query).startswith("Nothing to look up")


# ---- confidence markers ----------------------------------------------------------


def test_unverified_markers_are_kept_and_explained_once(base):
    result = base.search("Squin Hub towns")
    assert "- Its shops pay full price for armour. (unverified)" in result
    assert result.count(UNVERIFIED_NOTE) == 1 and result.endswith(UNVERIFIED_NOTE)
    assert len(shown(result)) >= 2


def test_no_explanation_without_a_marker(base):
    result = base.search("bleeding")
    assert "unverified" not in result


def test_the_explanation_counts_towards_the_budget(base):
    for budget in (300, 360, 420, 500):
        result = base.search("Squin", max_chars=budget)
        assert len(result) <= budget
        assert ("(unverified)" in result) == result.endswith(UNVERIFIED_NOTE)


# ---- malformed and half-written input --------------------------------------------


def test_missing_and_empty_directories(tmp_path):
    for directory in (tmp_path / "absent", tmp_path / "empty", tmp_path / "file.md"):
        if directory.name == "empty":
            directory.mkdir()
        if directory.name == "file.md":
            directory.write_text("# Not a directory\n", encoding="utf-8")
        kb = KnowledgeBase(directory)
        assert kb.sections == []
        assert kb.search("anything").startswith("The Kenshi reference is empty")
        assert kb.topics().startswith("The Kenshi reference is empty")


def test_only_markdown_files_are_read(tmp_path):
    directory = tmp_path / "kb"
    write(directory, "notes.md", "# Notes\n\nNotes.\n\n## Real\n- Kept.\n")
    write(directory, "notes.txt", "# Text\n\n## Ignored text\n- No.\n")
    write(directory, ".hidden.md", "# Hidden\n\n## Ignored hidden\n- No.\n")
    (directory / "folder.md").mkdir()
    assert [section.heading for section in KnowledgeBase(directory).sections] == ["Real"]


def test_half_written_files(tmp_path):
    directory = tmp_path / "kb"
    write(directory, "empty.md", "")
    write(directory, "title-only.md", "# Just a title")
    write(directory, "no-body-yet.md", "# Started\n\nIt covers things.\n\n## First heading")
    write(
        directory,
        "mid-line.md",
        "# Cut\n\nCut off.\n\n## Whole\n- Complete bullet.\n\n## Partial\n- This bullet stops mid-wo",
    )
    cut_inside_a_character = "# Bytes\n\nBytes.\n\n## Caf\u00e9\n- Costs 5 cats \u2014".encode()[:-1]
    (directory / "mid-character.md").write_bytes(cut_inside_a_character)
    kb = KnowledgeBase(directory)
    by_file = {}
    for section in kb.sections:
        by_file.setdefault(section.source, []).append(section.heading)
    assert by_file == {"mid-line.md": ["Whole", "Partial"], "mid-character.md": ["Caf\u00e9"]}
    assert "\ufffd" not in kb.search("cafe")
    assert shown(kb.search("cafe")) == ["Bytes > Caf\u00e9"]
    index = kb.topics()
    assert "Just a title" in index and "Started: It covers things." in index and "(no sections yet)" in index


def test_a_file_without_a_title_is_named_after_its_file(tmp_path):
    kb = one_file(tmp_path, "## Lone section\n- A fact.\n", name="weapons_and-armour.md")
    assert [section.label for section in kb.sections] == ["Weapons and armour > Lone section"]


def test_format_drift_is_tolerated(tmp_path):
    kb = one_file(
        tmp_path,
        "\ufeff# Drift #\r\n"
        "Covers drift.\r\n"
        "- A stray bullet before any section.\r\n"
        "\r\n"
        "##No space after the hashes\r\n"
        "**Also:** spaceless, cramped\r\n"
        "- First.\r\n"
        "\r\n"
        "## **Bold heading:**\r\n"
        "\r\n"
        "- also: lower case, after a blank line\r\n"
        "- Second.\r\n"
        "### A small sub-heading\r\n"
        "- Third, still part of the bold heading section.\r\n"
        "\r\n"
        "## 3. Numbered heading\r\n"
        "```\r\n"
        "## not a heading, it is inside a code block\r\n"
        "```\r\n"
        "\r\n"
        "# A second top-level heading\r\n"
        "Plain text rather than bullets.\r\n"
        "\r\n"
        "## SOURCES:\r\n"
        "- https://example.org\r\n",
    )
    sections = {section.heading: section for section in kb.sections}
    assert list(sections) == [
        "Overview",
        "No space after the hashes",
        "Bold heading",
        "Numbered heading",
        "A second top-level heading",
    ]
    assert all(section.title == "Drift" for section in sections.values())
    assert sections["No space after the hashes"].also == "spaceless, cramped"
    assert sections["Bold heading"].also == "lower case, after a blank line"
    assert sections["Bold heading"].body == (
        "- Second.\n### A small sub-heading\n- Third, still part of the bold heading section."
    )
    assert "## not a heading" in sections["Numbered heading"].body
    assert shown(kb.search("cramped")) == ["Drift > No space after the hashes"]
    assert "Drift: Covers drift." in kb.topics()


def test_a_long_section_with_sub_headings_is_split_at_them(tmp_path):
    part = "".join(f"- Detail {i} of this part, padded out to a realistic bullet length.\n" for i in range(18))
    kb = one_file(
        tmp_path,
        f"# Big\n\nBig sections.\n\n## Weapons\nAlso: arms\n- Kinds of weapon.\n### Katanas\n{part}### Sabres\n{part}",
    )
    assert [section.heading for section in kb.sections] == ["Weapons", "Weapons: Katanas", "Weapons: Sabres"]
    assert shown(kb.search("sabers"))[0] == "Big > Weapons: Sabres"


# ---- topics ----------------------------------------------------------------------


def test_topics_lists_every_file_with_its_description_and_headings(base):
    index = base.topics()
    assert index.startswith("Kenshi reference: 8 sections in 3 files.")
    assert "\nControls: What the buttons on the screen do.\n  Hold button; Passive button\n" in index
    assert "\nTowns and traders: Where the towns are and what their shops buy and sell.\n" in index
    assert "  The Hub (town); Squin (town); Selling items to a trader" in index
    assert "Also:" not in index and "- " not in index


def test_topics_can_be_narrowed_to_one_file(base):
    for wanted in ("medical", "Medical.md", " MEDIC "):
        index = base.topics(file=wanted)
        assert index.startswith("Kenshi reference: 3 sections in 1 file matching")
        assert "Bleeding and bandaging; Beds and resting; Bonedogs" in index
        assert "Controls" not in index and "Towns" not in index
    assert base.topics(file="traders").count("\n\n") == 1  # matched by title
    missing = base.topics(file="spaceships")
    assert missing == (
        'No file of the Kenshi reference matches "spaceships". '
        "The files are: Controls; Medical; Towns and traders."
    )


def test_topics_stays_small_for_a_large_knowledge_base(tmp_path):
    directory = tmp_path / "kb"
    for number in range(8):
        sections = "".join(
            f"## Section {number}-{i} on a subject\n- A fact.\n\n" for i in range(150)
        )
        write(directory, f"file{number}.md", f"# File {number}\n\nThe subject of file {number}.\n\n{sections}")
    kb = KnowledgeBase(directory)
    assert len(kb.sections) == 1200
    index = kb.topics()
    assert len(index) <= 12000
    for number in range(8):
        assert f"File {number}: The subject of file {number}." in index
        assert f"Section {number}-0 on" in index
    assert "; and " in index and " more" in index
    assert len(kb.topics(max_chars=2000)) <= 2000
    whole = kb.topics(file="file3")  # one file fits whole
    assert "Section 3-149 on" in whole and " more" not in whole and "File 4" not in whole
    # A few hundred sections fit whole.
    for path in sorted(directory.iterdir())[2:]:
        path.unlink()
    assert len(kb.sections) == 300
    assert " more" not in kb.topics() and "Section 1-149 on" in kb.topics()


# ---- caching ---------------------------------------------------------------------


def touch_later(path, seconds: int = 5) -> None:
    status = path.stat()
    os.utime(path, ns=(status.st_atime_ns, status.st_mtime_ns + seconds * 1_000_000_000))


def test_changes_on_disk_are_picked_up(tmp_path):
    directory = tmp_path / "kb"
    write(directory, "a.md", "# A\n\nFirst file.\n\n## Katanas\n- Sharp.\n")
    kb = KnowledgeBase(directory)
    assert shown(kb.search("katanas")) == ["A > Katanas"]
    assert shown(kb.search("crossbows")) == []

    write(directory, "b.md", "# B\n\nSecond file.\n\n## Crossbows\n- Ranged.\n")  # a new file
    assert shown(kb.search("crossbows")) == ["B > Crossbows"]

    write(directory, "a.md", "# A\n\nFirst file.\n\n## Katanas\n- Sharp.\n\n## Sabres\n- Curved.\n")  # a grown file
    assert shown(kb.search("sabres")) == ["A > Sabres"]

    write(directory, "b.md", "# B\n\nSecond file.\n\n## Longbows!\n- Ranged.\n")  # same size, later time
    touch_later(directory / "b.md")
    assert shown(kb.search("crossbows")) == [] and shown(kb.search("longbows")) == ["B > Longbows!"]

    (directory / "a.md").unlink()  # a removed file
    assert shown(kb.search("katanas")) == [] and len(kb.sections) == 1
    assert "A: First file." not in kb.topics()


def test_unchanged_files_are_not_parsed_again(tmp_path, monkeypatch):
    directory = tmp_path / "kb"
    write(directory, "a.md", "# A\n\nFirst.\n\n## Katanas\n- Sharp.\n")
    write(directory, "b.md", "# B\n\nSecond.\n\n## Crossbows\n- Ranged.\n")
    parsed = []
    original = knowledge._parse

    def counting(text, fallback_title):
        parsed.append(fallback_title)
        return original(text, fallback_title)

    monkeypatch.setattr(knowledge, "_parse", counting)
    kb = KnowledgeBase(directory)
    kb.search("katanas"), kb.topics(), kb.search("crossbows"), kb.sections
    assert sorted(parsed) == ["A", "B"]
    write(directory, "b.md", "# B\n\nSecond.\n\n## Crossbows\n- Ranged.\n- Slow to reload.\n")
    kb.search("katanas"), kb.search("reload")
    assert sorted(parsed) == ["A", "B", "B"]


def test_searching_from_several_threads(base):
    results, errors = [], []

    def work():
        try:
            results.append(base.search("stop bleeding"))
        except Exception as exc:  # pragma: no cover - reported below
            errors.append(exc)

    threads = [threading.Thread(target=work) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert not errors and len(set(results)) == 1


# ---- the bundled reference ---------------------------------------------------------


def test_module_functions_read_the_bundled_directory(tmp_path, monkeypatch):
    assert knowledge.KNOWLEDGE_DIR.name == "knowledge"
    assert knowledge.KNOWLEDGE_DIR.parent.name == "kenshi_link"
    write(tmp_path / "one", "medical.md", MEDICAL)
    write(tmp_path / "two", "controls.md", CONTROLS)
    monkeypatch.setattr(knowledge, "KNOWLEDGE_DIR", tmp_path / "one")
    assert shown(knowledge.search("stop bleeding", limit=1, max_chars=2000)) == ["Medical > Bleeding and bandaging"]
    assert knowledge.topics().startswith("Kenshi reference: 3 sections in 1 file.")
    assert "No file" in knowledge.topics(file="controls")
    monkeypatch.setattr(knowledge, "KNOWLEDGE_DIR", tmp_path / "two")
    assert shown(knowledge.search("hold")) == ["Controls > Hold button"]
    assert "Hold button; Passive button" in knowledge.topics(max_chars=500, file="controls")
    monkeypatch.setattr(knowledge, "KNOWLEDGE_DIR", tmp_path / "none")
    assert knowledge.search("hold").startswith("The Kenshi reference is empty")
    assert knowledge.topics().startswith("The Kenshi reference is empty")


def test_the_real_knowledge_directory(tmp_path):
    """Passes with no files; when there are some, each must yield at least one section.

    The files may be being written while this runs, so it works on a copy taken at one
    moment, and a file that has no section with a bullet under it yet is left alone.
    """
    real = knowledge.KNOWLEDGE_DIR
    names = sorted(path.name for path in real.glob("*.md") if not path.name.startswith(".")) if real.is_dir() else []
    if not names:
        assert KnowledgeBase(real).sections == []
        assert knowledge.search("the hub").startswith("The Kenshi reference is empty")
        return
    copy = tmp_path / "copy"
    copy.mkdir()
    started = []
    for name in names:
        data = (real / name).read_bytes()
        (copy / name).write_bytes(data)
        if re.search(r"^## (?!Sources\b).*\n(?:.*\n)*?- \S", data.decode("utf-8", errors="replace"), re.MULTILINE):
            started.append(name)
    kb = KnowledgeBase(copy)
    sections = kb.sections
    parsed = {section.source for section in sections}
    assert [name for name in started if name not in parsed] == [], "files with no usable section"
    for section in sections:
        assert section.title and section.heading and section.body.strip(), section.label
        assert section.heading.lower() != "sources", section.label
    # A section can be found by its own heading (checked on a spread of about 60 sections).
    for section in sections[:: max(1, len(sections) // 60)]:
        assert section.text in kb.search(section.heading, limit=20, max_chars=10**6), section.label
    assert len(kb.topics()) <= 12000
    for name in parsed:
        assert kb.topics(file=name).count("\n\n") >= 1, name
    result = kb.search("where to sell copper ore near the Hub", max_chars=3000)
    assert isinstance(result, str) and 0 < len(result) <= 3000
    assert isinstance(knowledge.search("where to sell copper ore near the Hub"), str)
