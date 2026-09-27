from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

icons = {
    "tbank": ("#FFDD2D", "#1C1C1E", "Т"),
    "alfabank": ("#EF3124", "#FFFFFF", "А"),
    "sberbank": ("#21A038", "#FFFFFF", "С"),
    "youtube": ("#FF0000", "#FFFFFF", "YT"),
    "vk": ("#0077FF", "#FFFFFF", "VK"),
    "vk-music": ("#FC2C38", "#FFFFFF", "♪"),
    "vk-video": ("#2683ED", "#FFFFFF", "▶"),
    "vtb": ("#009FDF", "#FFFFFF", "ВТБ"),
    "yandex-music": ("#FFCC00", "#1C1C1E", "Я"),
    "max": ("#6C5CE7", "#FFFFFF", "M"),
    "rave": ("#FF2D55", "#FFFFFF", "R"),
    "ok": ("#EE8208", "#FFFFFF", "OK"),
    "minecraft": ("#5D9C3E", "#FFFFFF", "MC"),
    "nulls-brawl": ("#1B9CFC", "#FFFFFF", "NB"),
}

out = Path("public/icons")
out.mkdir(parents=True, exist_ok=True)

try:
    font_lg = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
    font_sm = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
except Exception:
    font_lg = font_sm = ImageFont.load_default()

size = 128
for sid, (bg, fg, letter) in icons.items():
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=28, fill=bg)
    font = font_sm if len(letter) > 1 else font_lg
    bbox = d.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2, (size - th) / 2 - 4), letter, fill=fg, font=font)
    img.save(out / f"{sid}.webp", "WEBP", quality=90)
    print(sid)

print("webp icons done")
