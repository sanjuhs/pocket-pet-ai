"""Build the side-by-side source/implementation board used for visual QA."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "design/qa/comparison-board-v2.png"
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


comparisons = [
    (ROOT / "design/references/option-3-living-object.png", "SOURCE · OPTION 3"),
    (ROOT / "design/qa/final-hero.png", "IMPLEMENTATION · HERO"),
    (ROOT / "design/references/option-3-living-object.png", "SOURCE · OPTION 3"),
    (ROOT / "design/qa/final-hardware.png", "IMPLEMENTATION · PRODUCT STORY"),
    (ROOT / "design/references/option-3-living-object.png", "SOURCE · OPTION 3"),
    (ROOT / "design/qa/final-principles.png", "IMPLEMENTATION · PRINCIPLES + EVIDENCE"),
    (ROOT / "design/references/option-2-dark-product-theatre.png", "SOURCE · OPTION 2 ENDING"),
    (ROOT / "design/qa/final-architecture.png", "IMPLEMENTATION · ARCHITECTURE"),
    (ROOT / "design/references/option-2-dark-product-theatre.png", "SOURCE · OPTION 2 ENDING"),
    (ROOT / "design/qa/final-evidence.png", "IMPLEMENTATION · PROOF"),
    (ROOT / "design/references/option-2-dark-product-theatre.png", "SOURCE · OPTION 2 ENDING"),
    (ROOT / "design/qa/final-footer.png", "IMPLEMENTATION · RESEARCH + FOOTER"),
]

board = Image.new("RGB", (PANEL[0] * 2 + 36, PANEL[1] * 6 + 84), "#dedbd4")
for index, item in enumerate(comparisons):
    column = index % 2
    row = index // 2
    board.paste(tile(*item), (12 + column * (PANEL[0] + 12), 12 + row * (PANEL[1] + 12)))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
board.save(OUTPUT, optimize=True)
print(OUTPUT)
