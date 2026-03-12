from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


SIZE = 1024
BG = "#050505"
BLUE = "#12A8FF"
YELLOW = "#FFD400"


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def main() -> None:
    root = Path(__file__).resolve().parent
    assets = root / "assets"
    assets.mkdir(exist_ok=True)

    image = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)

    rounded_rect(draw, (92, 92, 932, 932), 190, "#0E0E0E")
    rounded_rect(draw, (120, 120, 904, 904), 170, "#000000")

    # Video frame
    rounded_rect(draw, (170, 250, 590, 760), 62, BLUE)
    rounded_rect(draw, (205, 285, 555, 725), 44, BG)

    # Play symbol
    draw.polygon([(305, 355), (305, 655), (505, 505)], fill=BLUE)

    # Speaker body
    draw.polygon(
        [(650, 430), (730, 430), (800, 365), (800, 645), (730, 580), (650, 580)],
        fill=YELLOW,
    )

    # Sound waves
    for inset in (0, 64, 128):
        draw.arc(
            (710 + inset, 290 + inset // 2, 980 - inset // 2, 720 - inset // 2),
            start=300,
            end=60,
            fill=YELLOW,
            width=26,
        )

    image.save(assets / "icon-1024.png")


if __name__ == "__main__":
    main()
