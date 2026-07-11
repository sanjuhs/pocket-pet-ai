"""Build the side-by-side source/implementation board used for visual QA."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "design/qa/comparison-board-v1.png"
PANEL = (620, 620)


def tile(path: Path, label: str) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail((PANEL[0], PANEL[1] - 42), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", PANEL, "#f2f0eb")
    x = (PANEL[0] - image.width) // 2
    canvas.paste(image, (x, 42))
    draw = ImageDraw.Draw(canvas)
    draw.text((16, 14), label, fill="#121212", font=ImageFont.load_default())
    return ImageOps.expand(canvas, border=1, fill="#c8c4bc")


sources = [
    (ROOT / "design/references/option-3-living-object.png", "SOURCE · OPTION 3"),
    (ROOT / "design/references/option-2-dark-product-theatre.png", "SOURCE · OPTION 2 ENDING"),
]
implementations = [
    (ROOT / "design/qa/implementation-hero-v2.png", "IMPLEMENTATION · HERO"),
    (ROOT / "design/qa/implementation-story-listens.png", "IMPLEMENTATION · STORY"),
    (ROOT / "design/qa/implementation-technical.png", "IMPLEMENTATION · TECHNICAL"),
    (ROOT / "design/qa/implementation-footer-v2.png", "IMPLEMENTATION · FINALE"),
]

board = Image.new("RGB", (PANEL[0] * 2 + 36, PANEL[1] * 3 + 48), "#dedbd4")
for index, item in enumerate(sources + implementations):
    column = index % 2
    row = index // 2
    board.paste(tile(*item), (12 + column * (PANEL[0] + 12), 12 + row * (PANEL[1] + 12)))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
board.save(OUTPUT, optimize=True)
print(OUTPUT)
