from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("public/icons")
SIZE = 256


def bold(sz: int):
    for p in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def canvas(bg: tuple[int, int, int]):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=57, fill=bg)
    return img, d


def save(img: Image.Image, name: str) -> None:
    img.save(OUT / name, "WEBP", quality=94)
    print(name, (OUT / name).stat().st_size)


def text_center(d, text, fill, size=64, dy=0):
    f = bold(size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((SIZE - tw) / 2, (SIZE - th) / 2 + dy), text, font=f, fill=fill)


# Minecraft
img, d = canvas((93, 156, 62))
d.rectangle([40, 40, 216, 96], fill=(110, 170, 55))
d.rectangle([40, 96, 216, 216], fill=(128, 90, 50))
for i in range(40, 216, 44):
    d.line([(i, 96), (i, 216)], fill=(95, 65, 35), width=3)
for i in range(96, 216, 44):
    d.line([(40, i), (216, i)], fill=(95, 65, 35), width=3)
save(img, "minecraft.webp")

# Alfa
img, d = canvas((239, 49, 36))
d.polygon([(128, 32), (222, 220), (34, 220)], fill=(255, 255, 255))
d.polygon([(128, 92), (182, 204), (74, 204)], fill=(239, 49, 36))
save(img, "alfabank.webp")

# VTB
img, d = canvas((0, 90, 170))
text_center(d, "ВТБ", (255, 255, 255), 72, -6)
save(img, "vtb.webp")

# VK
img, d = canvas((0, 119, 255))
text_center(d, "VK", (255, 255, 255), 86, -8)
save(img, "vk.webp")

# VK Music
img, d = canvas((252, 44, 56))
d.ellipse([58, 150, 118, 210], fill=(255, 255, 255))
d.ellipse([140, 128, 200, 188], fill=(255, 255, 255))
d.rectangle([106, 58, 120, 176], fill=(255, 255, 255))
d.rectangle([188, 42, 202, 154], fill=(255, 255, 255))
d.polygon([(120, 58), (202, 42), (202, 64), (120, 80)], fill=(255, 255, 255))
save(img, "vk-music.webp")

# VK Video
img, d = canvas((38, 131, 237))
d.rounded_rectangle([48, 70, 208, 186], radius=30, fill=(255, 255, 255))
d.polygon([(100, 100), (100, 156), (160, 128)], fill=(38, 131, 237))
save(img, "vk-video.webp")

# Yandex Music
img, d = canvas((255, 204, 0))
d.ellipse([68, 68, 188, 188], fill=(0, 0, 0))
d.ellipse([92, 92, 164, 164], fill=(255, 204, 0))
d.ellipse([110, 110, 146, 146], fill=(0, 0, 0))
save(img, "yandex-music.webp")

# OK
img, d = canvas((238, 130, 8))
d.ellipse([78, 46, 178, 146], outline=(255, 255, 255), width=18)
d.arc([62, 118, 194, 222], 200, 340, fill=(255, 255, 255), width=18)
save(img, "ok.webp")

# MAX
img, d = canvas((92, 64, 214))
text_center(d, "MAX", (255, 255, 255), 60, -4)
d.polygon([(90, 88), (108, 114), (72, 114)], fill=(255, 204, 0))
d.polygon([(180, 140), (208, 112), (208, 168)], fill=(255, 204, 0))
save(img, "max.webp")

# Rave
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
for y in range(SIZE):
    t = y / (SIZE - 1)
    d.line(
        [(0, y), (SIZE, y)],
        fill=(int(255 - 100 * t), int(50 + 30 * t), int(160 + 60 * t), 255),
    )
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=57, fill=255)
out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
out.paste(img, mask=mask)
d = ImageDraw.Draw(out)
d.ellipse([74, 74, 182, 182], fill=(255, 255, 255))
d.polygon([(112, 104), (112, 152), (158, 128)], fill=(220, 40, 140))
save(out, "rave.webp")

# Null's Brawl
img, d = canvas((20, 120, 220))
d.ellipse([36, 36, 220, 220], fill=(255, 196, 0))
d.regular_polygon((128, 120, 52), n_sides=5, rotation=90, fill=(20, 100, 200))
text_center(d, "NB", (255, 255, 255), 40, 58)
save(img, "nulls-brawl.webp")

print("done")
