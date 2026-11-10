"""Search over the Kenshi reference files, for the model that is playing.

The reference is a set of Markdown files in the `knowledge` directory next to this module.
Each file is a `# Title`, one sentence saying what it covers, and `## ` sections; a section
is one retrievable unit: an optional `Also: ` line of synonyms and search terms, then short
bullets. A bullet that could not be confirmed ends with `(unverified)`. The closing
`## Sources` section lists URLs and is not searched.

`search(query)` returns the few sections that best answer a short natural-language query, as
text ready to hand to the model: each section whole, under a `## File title > Heading` line,
best first, within a character budget. When nothing matches well it says so and lists the
closest headings. `topics()` returns an index of everything available. Both read the files
on first use and again whenever a file changes on disk, so files can be added or edited
while the server runs. Neither raises for any query or any state of the directory.

The parser is forgiving, because the files are written by hand and may be read half-written:
a missing directory, an empty file, a file without a title, a heading with nothing under it,
deeper headings and a decorated `Also:` line are all accepted.

Only the standard library is used.
"""

from __future__ import annotations

import difflib
import functools
import math
import re
import threading
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

__all__ = ["KNOWLEDGE_DIR", "KnowledgeBase", "Match", "Section", "search", "topics"]

# Where the reference files live. search() and topics() read this each time they are called.
KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"

UNVERIFIED_NOTE = (
    "(unverified) marks a fact the writer could not confirm in a source: "
    "check it in the game before relying on it."
)

# ---- ranking parameters ------------------------------------------------------------
#
# Each query term scores either as a word of the heading, or as a search key plus its
# mentions in the body, whichever is more, plus a little for the file's title; rarer terms
# count for more (BM25). The total is then scaled by how many of the distinct query terms
# the section matched.
#
# A heading says what a section is about, so a word there settles it: how often the body
# repeats the word no longer matters, and the less else the heading says, the more the word
# counts ("The Hub (town)" is more about the Hub than "Where to mine near The Hub"). The
# `Also:` line is a list of search keys, and the words of the heading are keys too: a word
# is among them or not, however often it is repeated.

W_HEADING = 5.0  # times 1/2 for a heading of average weight, 2/3 for one half as heavy
W_ALSO = 2.0
W_BODY = 1.0  # times about 0.45 for one mention, 0.7 for three, never 1
W_TITLE = 0.4  # every section of a file gets this for a word of the file's title
K_BODY, B_BODY = 1.2, 0.6
PARTIAL = 0.5  # a related word form ("trade" for "trader") counts this much of an exact match
COVERAGE_FLOOR = 0.4  # score multiplier runs from this (one term of many) to 1 (all terms)
HEADING_FOCUS = 0.3  # extra share of the score when the heading holds every query word
RELATIVE_FLOOR = 0.5  # sections scoring below this share of the best one are not returned...
NAMED_FLOOR = 0.15  # ...unless they are the best section named for a query word, down to this
MENTION_FLOOR = 0.25  # sections down to this share are listed by heading as also relevant
NAMED_WEIGHT = 0.25  # how rare (as a share of the rarest possible) a word must be to name a section
SPECIFIC_WEIGHT = 0.5  # how rare a word in a heading must be for that alone to make a good match
QUALITY_FLOOR = 0.33  # below this, and with no specific heading hit, nothing "matches well"
MIN_CHARS = 300  # smallest character budget search() works to
SPLIT_ABOVE = 1800  # a section with sub-headings longer than this is split at them
MAX_TERMS = 16

# ---- words -------------------------------------------------------------------------

STOPWORDS = frozenset(
    """
    a an the and or but if then than so of to in on at by for from with without about as into onto
    is are was were be been being am do does did doing can could should would will shall may might
    must have has had having i me my we our us you your it its they them their he she his her him
    this that these those there here what which who whom whose when where why how
    up down out off over after before while during again near through between around
    not no any some also just very much many please tell explain mean means
    want wants need needs get gets getting got someone something anyone anything way
    happen happens happened work works
    ca wo dont cant wont im ive whats hows wheres doesnt isnt kenshi
    """.split()
)

# Forms the suffix rules cannot reach, and spellings that differ between British and American
# English (the game is British: "armour", "Defence"; the model asking may not be).
_IRREGULAR = {
    "ate": "eat", "eaten": "eat", "bled": "bleed", "bought": "buy", "broke": "break",
    "broken": "break", "built": "build", "caught": "catch", "children": "child", "dead": "die",
    "death": "die", "deaths": "die", "dying": "die", "fed": "feed", "feet": "foot",
    "fought": "fight", "found": "find", "gave": "give", "given": "give", "goes": "go",
    "gone": "go", "went": "go", "halves": "half", "held": "hold", "hid": "hide",
    "hidden": "hide", "hungry": "hunger", "knives": "knife", "lost": "lose", "lying": "lie",
    "made": "make", "men": "man", "menus": "menu", "paid": "pay", "ran": "run",
    "shelves": "shelf", "shot": "shoot", "slept": "sleep", "sold": "sell", "starvation": "starve",
    "stole": "steal", "stolen": "steal", "taken": "take", "took": "take", "teeth": "tooth",
    "thieves": "thief", "tying": "tie", "wolves": "wolf", "women": "woman", "wore": "wear",
    "worn": "wear",
    "ax": "axe", "centre": "center", "centres": "centers", "defence": "defense",
    "defences": "defenses", "dialogue": "dialog", "dialogues": "dialogs", "grey": "gray",
    "licence": "license", "metre": "meter", "metres": "meters", "offence": "offense",
    "sabre": "saber", "sabres": "sabers",
}
_OUR = re.compile(r"^(arm|behavi|col|fav|flav|harb|hon|hum|lab|neighb|od|rig|rum|sav|val|vap|vig)our")

_WORD = re.compile(r"[a-z0-9]+")
_LINK = re.compile(r"https?://\S+")
_CONTRACTION = re.compile(r"(?:n't|'(?:s|m|re|ve|ll|d))\b")
# Punctuation that ends a phrase: words on either side of it are not treated as neighbours.
_PHRASE_BREAK = re.compile(r"[\n\r,.;:!?()\[\]{}|/\\\"<>=+*]+|\s[-\u2013\u2014]+\s")


def _is_vowel(word: str, i: int) -> bool:
    ch = word[i]
    if ch in "aeiou":
        return True
    return ch == "y" and i > 0 and not _is_vowel(word, i - 1)


def _has_vowel(word: str) -> bool:
    return any(_is_vowel(word, i) for i in range(len(word)))


def _measure(word: str) -> int:
    """How many times a run of vowels is followed by a consonant (Porter's m)."""
    count, after_vowel = 0, False
    for i in range(len(word)):
        vowel = _is_vowel(word, i)
        if after_vowel and not vowel:
            count += 1
        after_vowel = vowel
    return count


def _ends_cvc(word: str) -> bool:
    """Consonant, vowel, consonant at the end, as in "min" or "trad" (but not -w, -x, -y)."""
    n = len(word)
    return (
        n >= 3
        and word[-1] not in "wxy"
        and not _is_vowel(word, n - 1)
        and _is_vowel(word, n - 2)
        and not _is_vowel(word, n - 3)
    )


def _tidy(base: str) -> str:
    """Repair what is left after removing -ed or -ing: stopp -> stop, min -> mine, us -> use."""
    if len(base) < 3:
        return base if base[-1] in "aeou" else base + "e"
    if base.endswith(("at", "bl", "iz")):
        return base + "e"
    if base[-1] == base[-2] and base[-1] not in "aeioulsz":
        return base[:-1] if len(base) > 3 else base
    if _measure(base) == 1 and _ends_cvc(base):
        return base + "e"
    return base


@functools.lru_cache(maxsize=65536)
def stem(word: str) -> str:
    """Reduce a lower-case word to a form shared by its plural, -ed and -ing forms.

    This is the inflectional part of Porter's stemmer (steps 1 and 5) with a table of
    irregular forms. It leaves derived words alone ("trader" stays apart from "trade");
    those are bridged at a discount when a query is matched.
    """
    w = _IRREGULAR.get(word, word)
    w = _OUR.sub(r"\1or", w)
    if len(w) < 3 or not w.isalpha():
        return w
    if len(w) > 3:
        if w.endswith("sses"):
            w = w[:-2]
        elif w.endswith("ies"):
            w = w[:-2] if len(w) > 4 else w[:-1]
        elif w.endswith("s") and not w.endswith(("ss", "us", "is")):
            w = w[:-1]
        if w.endswith("eed"):
            if _measure(w[:-3]) > 0:
                w = w[:-1]
        else:
            for suffix in ("ing", "ed"):
                base = w[: -len(suffix)]
                if w.endswith(suffix) and len(base) >= 2 and _has_vowel(base):
                    w = _tidy(base)
                    break
    if len(w) > 2 and w.endswith("y") and not _is_vowel(w, len(w) - 2):
        w = w[:-1] + "i"
    if w.endswith("e") and len(w) > 3:
        base = w[:-1]
        m = _measure(base)
        if m > 1 or (m == 1 and not _ends_cvc(base)):
            w = base
    if w.endswith("ll") and _measure(w[:-1]) > 1:
        w = w[:-1]
    return w


# Endings (as they look after stemming) that turn a word into a close relative of itself:
# trade/trader, safe/safest, medic/medical, injure/injury, quick/quickly, store/storage.
_ENDINGS = frozenset(
    "er r est st i li ti ri eri al ic in th ment ness ful ous ive ion ation abl ag ist".split()
)


def _akin(a: str, b: str) -> bool:
    """Whether two different stems look like forms of one word: the longer is the shorter
    plus a common ending. A shared beginning alone is not enough: "drag" begins "dragon"."""
    short, long = (a, b) if len(a) <= len(b) else (b, a)
    if a == b or len(short) < 4 or not short.isalpha():
        return False
    if long.startswith(short):
        return long[len(short) :] in _ENDINGS
    # A final e gives way to an ending that starts with a vowel: store -> stor(age).
    ending = long[len(short) - 1 :]
    return (
        short.endswith("e")
        and len(short) > 4
        and long.startswith(short[:-1])
        and ending[:1] in "aio"
        and ending in _ENDINGS
    )


def _phrases(text: str) -> list[list[str]]:
    """The words of a text that carry meaning, lower-cased and without accents, grouped into
    runs that no punctuation interrupts."""
    text = text.lower()
    if not text.isascii():
        text = unicodedata.normalize("NFKD", text.replace("\u2019", "'").replace("\u2018", "'"))
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = _CONTRACTION.sub("", _LINK.sub(" ", text)).replace("'", "")
    phrases = []
    for chunk in _PHRASE_BREAK.split(text):
        words = [
            word
            for word in _WORD.findall(chunk)
            if (len(word) > 1 or word.isdigit()) and word not in STOPWORDS
        ]
        if words:
            phrases.append(words)
    return phrases


def _analyse(text: str) -> tuple[Counter[str], list[str]]:
    """Index a text: counts of its stems, and the stems in order.

    The counts also hold every pair of neighbouring words written as one word, so that
    "Beak Thing" is found by "beakthing", "bonedog" by "bone dog", and a query whose words
    are neighbours in the text scores above one whose words are merely both present.
    """
    counts: Counter[str] = Counter()
    stems: list[str] = []
    for words in _phrases(text):
        for word in words:
            stems.append(stem(word))
        for first, second in zip(words, words[1:]):
            if first.isalpha() and second.isalpha():
                counts[stem(first + second)] += 1
    counts.update(stems)
    return counts, stems


# ---- parsing -----------------------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})(?!#)\s*(.*?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_ALSO = re.compile(
    r"^\s*(?:[-*+]\s+)?[*_`]*(?:also(?:\s+known\s+as)?|aka|aliases|synonyms|keywords)[*_`]*"
    r"\s*:[*_`]*\s*(.*?)[*_`]*\s*$",
    re.IGNORECASE,
)
_SOURCES = re.compile(
    r"^(sources?|references?|bibliography|citations?|(external\s+)?links)(\s+(and|&)\s+\w+)?$",
    re.IGNORECASE,
)
_SOURCE_WORD = re.compile(r"\b(sources?|references?|citations?|links|credits|further reading)\b", re.IGNORECASE)
_URL = re.compile(r"https?://", re.IGNORECASE)
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_UNVERIFIED = re.compile(r"\(\s*unverified\b[^)\n]*\)", re.IGNORECASE)


@dataclass(frozen=True)
class Section:
    """One retrievable unit of the reference: a `## ` section of one file."""

    source: str  # file name, such as "towns.md"
    title: str  # the file's `# ` title
    heading: str
    also: str  # the text of the section's `Also:` line, or ""
    body: str  # the section's lines, without the heading and the `Also:` line

    @property
    def label(self) -> str:
        return f"{self.title} > {self.heading}"

    @property
    def text(self) -> str:
        """The section as it is shown to the model."""
        return f"## {self.label}\n{self.body}"


@dataclass(frozen=True)
class Match:
    """A section that matched a query.

    `confident` is False for a match too thin to be shown on its own. `named` holds the
    query words (as stems) that the section's heading or `Also:` line contains in some
    form, leaving out words so common that they say nothing about what the section is.
    """

    section: Section
    score: float
    confident: bool
    named: frozenset[str] = frozenset()


class _Entry:
    """A section with its search terms worked out."""

    __slots__ = ("section", "heading", "heading_stems", "also", "body", "body_len", "title", "stems", "label_stems")

    def __init__(self, section: Section, title_terms: frozenset[str]) -> None:
        self.section = section
        self.heading, heading_stems = _analyse(section.heading)
        self.also, also_stems = _analyse(section.also)
        self.body, body_stems = _analyse(section.body)
        self.heading_stems = frozenset(heading_stems)
        self.body_len = len(body_stems)
        self.title = title_terms
        self.label_stems = self.heading_stems | frozenset(also_stems)
        self.stems = self.label_stems | frozenset(body_stems)


class _File:
    """One parsed knowledge file."""

    __slots__ = ("name", "stamp", "title", "description", "entries")

    def __init__(self, name: str, stamp: tuple[int, int], text: str) -> None:
        self.name = name
        self.stamp = stamp
        self.title, self.description, parts = _parse(text, _title_from_name(name))
        title_terms = frozenset(_analyse(self.title)[0])
        self.entries = [
            _Entry(Section(name, self.title, heading, also, body), title_terms)
            for heading, also, body in parts
        ]


def _title_from_name(name: str) -> str:
    words = re.sub(r"[-_]+", " ", Path(name).stem).strip()
    return words[:1].upper() + words[1:] if words else name


def _clean_heading(text: str) -> str:
    text = text.strip().strip("*_`").strip()
    text = re.sub(r"^\d+[.)]\s+", "", text)
    return " ".join(text.rstrip(":").split())


def _clean_body(lines: list[str]) -> str:
    out: list[str] = []
    for line in lines:
        line = line.rstrip()
        if line or (out and out[-1]):
            out.append(line)
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


def _is_sources(heading: str, lines: list[str]) -> bool:
    """The closing list of URLs: named so, or named roughly so and made mostly of links."""
    name = re.sub(r"\s*\(.*?\)\s*$", "", heading).strip()
    if _SOURCES.match(name):
        return True
    if _SOURCE_WORD.search(heading):
        filled = [line for line in lines if line.strip()]
        linked = sum(1 for line in filled if _URL.search(line))
        return linked >= 2 and linked * 2 >= len(filled)
    return False


def _split_also(lines: list[str]) -> tuple[str, list[str]]:
    """Take the `Also:` line off the top of a section, if it has one."""
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        found = _ALSO.match(line)
        if found:
            return found.group(1).strip(), lines[:i] + lines[i + 1 :]
        break
    return "", lines


def _parse(text: str, fallback_title: str) -> tuple[str, str, list[tuple[str, str, str]]]:
    """Split a knowledge file into its title, its description and (heading, also, body) parts."""
    title: str | None = None
    preamble: list[str] = []
    # Each block is a `## ` section: its heading, its lines, and where sub-headings start.
    blocks: list[tuple[str, list[str], list[tuple[int, str]]]] = []
    fenced = False
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        found = None
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            found = _HEADING.match(line)
        if found is None:
            (blocks[-1][1] if blocks else preamble).append(line)
            continue
        level, heading = len(found.group(1)), _clean_heading(found.group(2))
        if level == 1 and title is None and not blocks:
            title = heading or None
        elif level <= 2 or not blocks:
            blocks.append((heading, [], []))
        else:
            blocks[-1][2].append((len(blocks[-1][1]), heading))
            blocks[-1][1].append(line)

    # The description is the first paragraph under the title; anything more is an overview.
    while preamble and not preamble[0].strip():
        preamble.pop(0)
    end = next(
        (i for i, line in enumerate(preamble) if not line.strip() or (i and _LIST_ITEM.match(line))),
        len(preamble),
    )
    description = " ".join(" ".join(preamble[:end]).split())
    if any(line.strip() for line in preamble[end:]):
        blocks.insert(0, ("Overview", preamble[end:], []))

    parts: list[tuple[str, str, str]] = []
    for heading, lines, subs in blocks:
        if _is_sources(heading, lines):
            continue
        heading = heading or "(untitled)"
        pieces = [(heading, lines)]
        if subs and sum(len(line) + 1 for line in lines) > SPLIT_ABOVE:
            starts = [start for start, _ in subs] + [len(lines)]
            pieces = [(heading, lines[: starts[0]])]
            for (start, sub), stop in zip(subs, starts[1:]):
                pieces.append((f"{heading}: {sub}" if sub else heading, lines[start + 1 : stop]))
        for piece_heading, piece_lines in pieces:
            also, rest = _split_also(piece_lines)
            body = _clean_body(rest)
            if body:
                parts.append((piece_heading, also, body))
    return title or fallback_title, description, parts


def _read(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    # A file caught mid-write can end inside a multi-byte character.
    return data.decode("utf-8", errors="replace").lstrip("\ufeff").rstrip("\ufffd")


# ---- the index ---------------------------------------------------------------------


class _Term:
    """One distinct word of a query, with the index terms that count as matching it."""

    __slots__ = ("word", "stem", "exact", "partial", "found")

    def __init__(self, word: str, stemmed: str) -> None:
        self.word = word  # as typed, for messages
        self.stem = stemmed
        self.exact = {stemmed}  # the stem, and the word joined to each neighbour
        self.partial: tuple[str, ...] = ()  # related stems in the files
        self.found = False  # whether any section matched it


def _saturate(exact: int, partial: int, k: float) -> float:
    if exact:
        return exact / (exact + k)
    if partial:
        return PARTIAL * partial / (partial + k)
    return 0.0


def _count(counts: Counter[str], forms) -> int:
    return sum(counts[form] for form in forms if form in counts)


class _Index:
    """A snapshot of every parsed file, with what ranking needs. Never changed once built."""

    def __init__(self, files: list[_File]) -> None:
        self.files = files
        self.entries = [entry for file in files for entry in file.entries]
        count = len(self.entries) or 1
        self.mean_body = sum(entry.body_len for entry in self.entries) / count or 1.0
        # How much a heading says: its words, each weighed by how few headings share it, so
        # that "(town)" and "(region)" add little. Relative to the average heading.
        used_in = Counter(s for entry in self.entries for s in entry.heading_stems)
        masses = [
            sum(math.log(1 + (count - used_in[s] + 0.5) / (used_in[s] + 0.5)) for s in entry.heading_stems)
            for entry in self.entries
        ]
        mean = sum(masses) / count or 1.0
        self.heading_mass = [mass / mean for mass in masses]
        self.label_vocabulary = sorted({s for entry in self.entries for s in entry.label_stems})
        self.by_prefix: dict[str, list[str]] = {}
        for stemmed in sorted({s for entry in self.entries for s in entry.stems}):
            if len(stemmed) >= 4:
                self.by_prefix.setdefault(stemmed[:4], []).append(stemmed)

    def terms(self, query: str) -> list[_Term]:
        terms: dict[str, _Term] = {}
        for words in _phrases(query):
            stems = [stem(word) for word in words]
            for word, stemmed in zip(words, stems):
                terms.setdefault(stemmed, _Term(word, stemmed))
            for i in range(len(words) - 1):
                if words[i].isalpha() and words[i + 1].isalpha():
                    joined = stem(words[i] + words[i + 1])
                    terms[stems[i]].exact.add(joined)
                    terms[stems[i + 1]].exact.add(joined)
        chosen = list(terms.values())[:MAX_TERMS]
        for term in chosen:
            related = self.by_prefix.get(term.stem[:4], ())
            term.partial = tuple(other for other in related if _akin(term.stem, other))
        return chosen

    def rank(self, terms: list[_Term]) -> list[Match]:
        """Every section that matches any term, best first."""
        entries = self.entries
        total = len(entries)
        if not terms or not total:
            return []
        rarest = math.log(1 + (total - 0.5) / 1.5)  # the weight of a term found in one section

        columns = []
        for term in terms:
            rows, sections_with_term = [], 0
            for entry in entries:
                # Counts of the term itself, then of related forms where the term is absent,
                # in the heading, the `Also:` line, the body and the file's title.
                in_heading = _count(entry.heading, term.exact)
                in_also = _count(entry.also, term.exact)
                in_body = _count(entry.body, term.exact)
                row = (
                    in_heading,
                    0 if in_heading else _count(entry.heading, term.partial),
                    in_also,
                    0 if in_also else _count(entry.also, term.partial),
                    in_body,
                    0 if in_body else _count(entry.body, term.partial),
                    1 if not entry.title.isdisjoint(term.exact) else 0,
                    1 if not entry.title.isdisjoint(term.partial) else 0,
                )
                rows.append(row)
                sections_with_term += any(row)
            term.found = sections_with_term > 0
            weight = math.log(1 + (total - sections_with_term + 0.5) / (sections_with_term + 0.5))
            columns.append((term.stem, rows, weight, weight if term.found else rarest))
        possible = sum(importance for *_, importance in columns)

        matches = []
        for i, entry in enumerate(entries):
            heading_k = self.heading_mass[i]
            body_k = K_BODY * (1 - B_BODY + B_BODY * entry.body_len / self.mean_body)
            score = matched = quality = headed = 0.0
            specific = False
            named = []
            for stemmed, rows, weight, importance in columns:
                heading, heading_p, also, also_p, body, body_p, title, title_p = rows[i]
                key = 1.0 if heading or also else PARTIAL if heading_p or also_p else 0.0
                part = max(
                    W_HEADING * _saturate(heading, heading_p, heading_k),
                    W_ALSO * key + W_BODY * _saturate(body, body_p, body_k),
                ) + W_TITLE * (1.0 if title else PARTIAL if title_p else 0.0)
                if not part:
                    continue
                score += weight * part
                # A related form is half a match; the file's title alone hardly one at all.
                matched += 1.0 if heading or also or body else 0.5 if key or body_p else 0.25
                if key and weight >= NAMED_WEIGHT * rarest:
                    named.append(stemmed)
                if heading:
                    headed += importance
                # How well the term is answered: in the label, in the body, or only by the file.
                if heading or also:
                    answered = 1.0
                    specific = specific or weight >= SPECIFIC_WEIGHT * rarest
                elif body:
                    answered = 0.6
                elif title:
                    answered = 0.3
                else:
                    answered = PARTIAL * (1.0 if key else 0.6 if body_p else 0.3)
                quality += importance * answered
            if score <= 0:
                continue
            coverage = matched / len(columns)
            score *= COVERAGE_FLOOR + (1 - COVERAGE_FLOOR) * coverage
            score *= 1 + HEADING_FOCUS * (headed / possible) ** 2
            confident = specific or quality / possible >= QUALITY_FLOOR
            matches.append((-score, i, Match(entry.section, score, confident, frozenset(named))))
        matches.sort(key=lambda item: item[:2])
        return [match for _, _, match in matches]

    def near_misses(self, terms: list[_Term], limit: int) -> list[Section]:
        """The best sections for the heading and `Also:` words spelled most like each query
        word that was found nowhere: "Squin (town)" for "Skuin"."""
        picked: list[Section] = []
        for term in terms:
            if term.found or len(term.stem) < 4:
                continue
            # A slip rarely changes the first letter; without that test "drive" finds "river".
            alike = [word for word in self.label_vocabulary if word[0] == term.stem[0]]
            close = difflib.get_close_matches(term.stem, alike, n=2, cutoff=0.8)
            if not close:
                continue
            guess = _Term(term.word, term.stem)
            guess.exact = set(close)
            for match in self.rank([guess])[:2]:
                if match.section not in picked:
                    picked.append(match.section)
        return picked[:limit]


# ---- the public interface ------------------------------------------------------------


def _shorten(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 3].rstrip() + "..."


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _fit_lines(lines: list[str], room: int) -> list[str]:
    """As many of the leading lines as fit in `room` characters, joined by newlines."""
    kept, used = [], 0
    for line in lines:
        cost = len(line) + (1 if kept else 0)
        if used + cost > room:
            break
        kept.append(line)
        used += cost
    return kept


class KnowledgeBase:
    """The reference files in one directory, parsed on demand and re-read when they change."""

    def __init__(self, directory: str | Path | None = None) -> None:
        self._directory = Path(directory) if directory is not None else None
        self._lock = threading.Lock()
        self._files: dict[str, _File] = {}
        self._loaded_from: Path | None = None
        self._index: _Index | None = None

    @property
    def directory(self) -> Path:
        return self._directory if self._directory is not None else KNOWLEDGE_DIR

    # -- loading --

    def _load(self) -> _Index:
        """The current index, re-parsing only files whose modification time or size changed."""
        directory = self.directory
        with self._lock:
            stamps: dict[str, tuple[Path, tuple[int, int]]] = {}
            try:
                paths = sorted(directory.iterdir())
            except OSError:  # no such directory, or not a directory
                paths = []
            for path in paths:
                if path.suffix.lower() != ".md" or path.name.startswith((".", "~")):
                    continue
                try:
                    status = path.stat()
                except OSError:
                    continue
                if path.is_file():
                    stamps[path.name] = (path, (status.st_mtime_ns, status.st_size))

            previous = self._files if directory == self._loaded_from else {}
            files: dict[str, _File] = {}
            changed = (
                self._index is None or directory != self._loaded_from or previous.keys() != stamps.keys()
            )
            for name, (path, stamp) in stamps.items():
                cached = previous.get(name)
                if cached is not None and cached.stamp == stamp:
                    files[name] = cached
                    continue
                changed = True
                text = _read(path)
                if text is not None:
                    files[name] = _File(name, stamp, text)
            if changed:
                self._files = files
                self._loaded_from = directory
                self._index = _Index(list(files.values()))
            assert self._index is not None
            return self._index

    @property
    def sections(self) -> list[Section]:
        """Every searchable section, in file and reading order."""
        return [entry.section for entry in self._load().entries]

    def rank(self, query: str) -> list[Match]:
        """Every section that matches the query, best first."""
        index = self._load()
        return index.rank(index.terms(query))

    # -- search --

    def search(self, query: str, limit: int = 4, max_chars: int = 6000) -> str:
        """The sections that best answer `query`, most relevant first, as text for the model.

        At most `limit` sections are returned and the whole text stays within `max_chars`
        (budgets under 300 are treated as 300): sections are included whole or not at all,
        except that a best section longer than the budget is cut at a line break. When
        nothing matches well the text says so and lists the closest headings instead.
        """
        index = self._load()
        if not index.entries:
            return f"The Kenshi reference is empty: no sections found in {self.directory}."
        query = " ".join(str(query or "").split())
        terms = index.terms(query)
        if not terms:
            return (
                "Nothing to look up: the query has no words to search for. Give a few specific "
                "words, such as a place, an item or what you are trying to do."
            )
        limit = max(1, int(limit))
        budget = max(MIN_CHARS, int(max_chars))
        matches = index.rank(terms)
        missing = [term.word for term in terms if not term.found]
        absent = "No section mentions: " + ", ".join(missing) + "." if missing else ""

        if not any(match.confident for match in matches[:3]):
            return self._no_match(index, query, terms, matches, absent, budget)

        # Keep the sections that score near the best one, and below those the best section
        # named for each query word that none of them is named for: for "weather hazards in
        # Venge" that is the Venge section, behind the one that lists hazards by region.
        best = matches[0].score
        worthwhile: list[Match] = []
        named: set[str] = set()
        for match in matches:
            if match.score >= RELATIVE_FLOOR * best or (
                match.score >= NAMED_FLOOR * best and not match.named <= named
            ):
                worthwhile.append(match)
                named |= match.named

        def pointers(left_out: list[Match]) -> list[str]:
            """One-line notes on what is not shown: further sections, and words found nowhere."""
            others = left_out + worthwhile[limit:]
            others += [m for m in matches if m.score >= MENTION_FLOOR * best and m not in worthwhile]
            lines = []
            if others:
                lines.append("Also relevant, not shown: " + "; ".join(m.section.label for m in others[:4]) + ".")
            if absent:
                lines.append(absent)
            return lines

        blocks: list[str] = []
        left_out: list[Match] = []
        used = 0
        flagged = False  # whether a shown section carries (unverified), which costs a note
        note_cost = len(UNVERIFIED_NOTE) + 2
        for match in worthwhile[:limit]:
            block = match.section.text
            cost = len(block) + (2 if blocks else 0)
            marked = _UNVERIFIED.search(block) is not None
            extra = note_cost if marked and not flagged else 0
            if used + cost + extra <= budget:
                blocks.append(block)
                used += cost + extra
                flagged = flagged or marked
            elif blocks:
                left_out.append(match)
            else:
                # Even the best section is over the budget: give as much of it as fits, alone,
                # keeping room for the pointers unless they would take much of the budget.
                left_out = worthwhile[1:limit]
                reserve = sum(len(line) + 1 for line in pointers(left_out)) + 1
                mark = "[Section cut here to fit the length limit.]"
                room = budget - len(mark) - 1 - (reserve if reserve <= budget // 3 else 0)
                lines = block.split("\n")
                kept = _fit_lines(lines, room)
                if _UNVERIFIED.search("\n".join(kept)):
                    kept = _fit_lines(lines, room - note_cost)
                    flagged = _UNVERIFIED.search("\n".join(kept)) is not None
                kept = kept or [_shorten(lines[0], room)]
                blocks.append("\n".join(kept + [mark]))
                used = len(blocks[0]) + (note_cost if flagged else 0)
                break

        # The pointers go in as far as the budget allows; the note on (unverified) is paid for.
        text = "\n\n".join(blocks)
        tail: list[str] = []
        for note in pointers(left_out):
            cost = len(note) + (1 if tail else 2)
            if used + cost <= budget:
                tail.append(note)
                used += cost
        if flagged:
            tail.append(UNVERIFIED_NOTE)
        return text + ("\n\n" + "\n".join(tail) if tail else "")

    def _no_match(
        self, index: _Index, query: str, terms: list[_Term], matches: list[Match], absent: str, budget: int
    ) -> str:
        shown = _shorten(query, 80)
        closest = index.near_misses(terms, limit=4)  # a misspelled name is the likeliest cause
        for match in matches[:5]:
            if match.section not in closest:
                closest.append(match.section)
        if not closest:
            lines = [f'Nothing in the Kenshi reference matches "{shown}".']
            if absent:
                lines.append(absent)
            lines.append("Try the words the game itself uses, or look through the topics index.")
            return "\n".join(_fit_lines(lines, budget))
        lines = [f'No section of the Kenshi reference matches "{shown}" well.', "Closest headings:"]
        lines += [f"- {section.label}" for section in closest[:6]]
        if absent:
            lines.append(absent)
        lines.append("Search again with one of these headings, or with the words the game itself uses.")
        return "\n".join(_fit_lines(lines, budget))

    # -- topics --

    def topics(self, max_chars: int = 12000, file: str = "") -> str:
        """An index of the reference: each file's title and description with its headings.

        Every heading is listed while the text fits in `max_chars`. Past that, which takes
        several hundred sections, each file's list is cut to the same length and says how
        many more headings there are. `file` narrows the index to the files whose name or
        title contains it, which is the way to read a list that was cut.
        """
        index = self._load()
        if not index.files:
            return f"The Kenshi reference is empty: no knowledge files found in {self.directory}."
        wanted = " ".join(str(file or "").lower().split()).removesuffix(".md")
        files = [f for f in index.files if wanted in Path(f.name).stem.lower() or wanted in f.title.lower()]
        if not files:
            titles = "; ".join(f.title for f in index.files)
            return f'No file of the Kenshi reference matches "{_shorten(wanted, 60)}". The files are: {titles}.'
        sections = sum(len(f.entries) for f in files)
        head = f"Kenshi reference: {_plural(sections, 'section')} in {_plural(len(files), 'file')}"
        head += f' matching "{_shorten(wanted, 60)}".' if wanted else "."
        head += " Look things up with a few words; the headings below show what is covered."

        def render(cap: int | None) -> str:
            lines = [head]
            for f in files:
                lines.append("")
                description = _shorten(f.description, 300)
                lines.append(f"{f.title}: {description}" if description else f.title)
                headings = [entry.section.heading for entry in f.entries]
                if not headings:
                    lines.append("  (no sections yet)")
                    continue
                shown = headings if cap is None else headings[:cap]
                listed = "; ".join(shown)
                more = len(headings) - len(shown)
                if more and shown:
                    listed += f"; and {more} more"
                elif more:
                    listed = _plural(more, "section")
                lines.append("  " + listed)
            return "\n".join(lines)

        text = render(None)
        if len(text) <= max_chars:
            return text
        low, high = 0, max(len(f.entries) for f in files)
        while low < high:  # the largest per-file cap that fits
            middle = (low + high + 1) // 2
            if len(render(middle)) <= max_chars:
                low = middle
            else:
                high = middle - 1
        return render(low)


_DEFAULT = KnowledgeBase()


def search(query: str, limit: int = 4, max_chars: int = 6000) -> str:
    """Search the bundled reference: see KnowledgeBase.search."""
    return _DEFAULT.search(query, limit, max_chars)


def topics(max_chars: int = 12000, file: str = "") -> str:
    """Index the bundled reference: see KnowledgeBase.topics."""
    return _DEFAULT.topics(max_chars, file)
