"""Screenshot scaling, encoding, overlays and the frame-difference motion measure."""

from __future__ import annotations

import io
import math
from dataclasses import dataclass

from PIL import Image, ImageChops, ImageDraw, ImageFont

# Limits Claude's vision input enforces on current models: an image over either
# one is rejected by the API rather than downscaled.
API_MAX_LONG_EDGE = 2576
API_MAX_VISUAL_TOKENS = 4784
_PATCH = 28


def visual_tokens(width: int, height: int) -> int:
    return math.ceil(width / _PATCH) * math.ceil(height / _PATCH)


@dataclass(frozen=True)
class Fit:
    """How a window's client area maps onto the image Claude sees."""

    scale: float  # image pixels per window pixel (<= 1)
    width: int
    height: int

    def to_window(self, x: float, y: float) -> tuple[int, int]:
        return round(x / self.scale), round(y / self.scale)

    def to_image(self, x: float, y: float) -> tuple[int, int]:
        return round(x * self.scale), round(y * self.scale)


def fit(width: int, height: int, max_long_edge: int) -> Fit:
    """Scale (width, height) down, never up, to respect max_long_edge and the API limits."""
    if width <= 0 or height <= 0:
        raise ValueError(f"window has no area ({width}x{height})")
    limit = max(64, min(max_long_edge, API_MAX_LONG_EDGE))
    scale = min(1.0, limit / max(width, height))
    while True:
        w = max(1, round(width * scale))
        h = max(1, round(height * scale))
        if visual_tokens(w, h) <= API_MAX_VISUAL_TOKENS:
            return Fit(scale=w / width, width=w, height=h)
        scale *= 0.97


def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    if image.size == size:
        return image
    return image.resize(size, Image.Resampling.LANCZOS)


def encode(image: Image.Image, fmt: str = "jpeg", quality: int = 80) -> tuple[bytes, str]:
    """Return (bytes, format name) for an RGB image."""
    buffer = io.BytesIO()
    fmt = fmt.lower()
    if fmt in ("jpg", "jpeg"):
        image.convert("RGB").save(buffer, format="JPEG", quality=quality, optimize=True)
        return buffer.getvalue(), "jpeg"
    if fmt == "png":
        image.convert("RGB").save(buffer, format="PNG", optimize=True)
        return buffer.getvalue(), "png"
    raise ValueError(f"unsupported image format {fmt!r} (use 'jpeg' or 'png')")


def _font(size: int) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def draw_grid(image: Image.Image, step: int = 100) -> Image.Image:
    """Overlay a labelled coordinate grid so positions can be read off the image."""
    out = image.convert("RGB").copy()
    draw = ImageDraw.Draw(out, "RGBA")
    font = _font(11)
    width, height = out.size
    for x in range(step, width, step):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 0, 90), width=1)
        draw.rectangle([x + 2, 2, x + 30, 15], fill=(0, 0, 0, 150))
        draw.text((x + 4, 2), str(x), fill=(255, 255, 0, 255), font=font)
    for y in range(step, height, step):
        draw.line([(0, y), (width, y)], fill=(255, 255, 0, 90), width=1)
        draw.rectangle([2, y + 2, 30, y + 15], fill=(0, 0, 0, 150))
        draw.text((4, y + 2), str(y), fill=(255, 255, 0, 255), font=font)
    return out


def draw_marker(image: Image.Image, x: int, y: int) -> Image.Image:
    """Ring the spot where the last pointer action landed (the OS cursor is not captured)."""
    out = image.convert("RGB").copy()
    draw = ImageDraw.Draw(out, "RGBA")
    for radius, colour in ((9, (0, 0, 0, 220)), (8, (255, 0, 255, 255)), (7, (0, 0, 0, 220))):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline=colour, width=1)
    draw.line([(x - 3, y), (x + 3, y)], fill=(255, 0, 255, 255), width=1)
    draw.line([(x, y - 3), (x, y + 3)], fill=(255, 0, 255, 255), width=1)
    return out


def motion_fraction(before: Image.Image, after: Image.Image) -> float:
    """Fraction (0..1) of pixels that changed between two frames.

    Screen grabs of a paused game are pixel-identical, so this is compared at full
    resolution: even one walking figure in a wide shot has to register.
    """
    if before.size != after.size:
        return 1.0
    a, b = before.convert("L"), after.convert("L")
    if max(a.size) > 1600:
        half = (a.width // 2, a.height // 2)
        a = a.resize(half, Image.Resampling.BOX)
        b = b.resize(half, Image.Resampling.BOX)
    histogram = ImageChops.difference(a, b).histogram()
    changed = sum(histogram[10:])
    return changed / (a.width * a.height)


def filmstrip(frames: list[Image.Image], height: int = 240) -> Image.Image | None:
    """Join frames left to right into one small strip, oldest first."""
    if not frames:
        return None
    thumbs = []
    for frame in frames:
        width = max(1, round(frame.width * height / frame.height))
        thumbs.append(frame.convert("RGB").resize((width, height), Image.Resampling.BILINEAR))
    gap = 4
    total = sum(t.width for t in thumbs) + gap * (len(thumbs) - 1)
    strip = Image.new("RGB", (total, height), (255, 255, 255))
    x = 0
    for thumb in thumbs:
        strip.paste(thumb, (x, 0))
        x += thumb.width + gap
    return strip
