"""Build polished brand icons for all apps."""
from __future__ import annotations

import io
import json
import ssl
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)
CTX = ssl.create_default_context()
SIZE = 256


def http_get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "image/*,*/*"},
    )
    with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
        data = r.read()
    if len(data) < 300:
        raise ValueError("small")
    return data


def itunes(app_id: int) -> bytes | None:
    try:
        meta = json.loads(http_get(f"https://itunes.apple.com/lookup?id={app_id}"))
        results = meta.get("results") or []
        if not results:
            return None
        art = results[0].get("artworkUrl512")
        if not art:
            return None
        art = art.replace("512x512bb", "1024x1024bb")
        return http_get(art)
    except Exception:
        return None


def save(raw: bytes, name: str) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    img.save(OUT / name, "WEBP", quality=93)
    print(f"  saved {name} ({(OUT / name).stat().st_size})")


def bold(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def canvas(bg: tuple[int, int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=57, fill=bg)
    return img, d


def center_text(d: ImageDraw.ImageDraw, text: str, fill, size: int = 64, dy: int = 0) -> None:
    f = bold(size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((SIZE - tw) / 2, (SIZE - th) / 2 + dy), text, font=f, fill=fill)


def write(img: Image.Image, name: str) -> None:
    img.save(OUT / name, "WEBP", quality=93)
    print(f"  drawn {name} ({(OUT / name).stat().st_size})")


def make_all() -> None:
    # --- App Store first ---
    store = {
        "youtube.webp": 544007664,
        "minecraft.webp": 479516143,
        "vk.webp": 564177498,
        "ok.webp": 401271034,
        "yandex-music.webp": 518133398,
        "tbank.webp": 1360253417,
        "rave.webp": 1129958305,
        "alfabank.webp": 1217378858,
        "sberbank.webp": 492394852,
        "vtb.webp": 585408566,
    }
    for name, aid in store.items():
        print(f"[{name}] itunes {aid}")
        raw = itunes(aid)
        if raw:
            save(raw, name)
        else:
            print("  miss")

    # --- Brand drawings for anything missing / weak ---
    # T-Bank yellow shield
    if (OUT / "tbank.webp").stat().st_size < 3000:
        img, d = canvas((255, 221, 45))
        # dark shield
        d.rounded_rectangle([68, 48, 188, 210], radius=28, fill=(30, 30, 30))
        d.rounded_rectangle([78, 58, 178, 200], radius=22, outline=(255, 221, 45), width=6)
        write(img, "tbank.webp")

    # Sber green
    if (OUT / "sberbank.webp").stat().st_size < 3000:
        img, d = canvas((21, 160, 56))
        d.arc([46, 46, 210, 210], 210, 60, fill=(255, 255, 255), width=24)
        d.ellipse([152, 62, 196, 106], fill=(255, 255, 255))
        write(img, "sberbank.webp")

    # Alfa red A
    if (OUT / "alfabank.webp").stat().st_size < 3000:
        img, d = canvas((239, 49, 36))
        d.polygon([(128, 36), (218, 214), (38, 214)], fill=(255, 255, 255))
        d.polygon([(128, 90), (178, 198), (78, 198)], fill=(239, 49, 36))
        write(img, "alfabank.webp")

    # VTB
    if (OUT / "vtb.webp").stat().st_size < 3000:
        img, d = canvas((0, 90, 170))
        center_text(d, "ВТБ", (255, 255, 255), 70, -4)
        write(img, "vtb.webp")

    # VK blue
    if (OUT / "vk.webp").stat().st_size < 3000:
        img, d = canvas((0, 119, 255))
        center_text(d, "VK", (255, 255, 255), 84, -6)
        write(img, "vk.webp")

    # VK Music red
    img, d = canvas((252, 44, 56))
    d.ellipse([58, 150, 118, 210], fill=(255, 255, 255))
    d.ellipse([140, 128, 200, 188], fill=(255, 255, 255))
    d.rectangle([106, 58, 120, 176], fill=(255, 255, 255))
    d.rectangle([188, 42, 202, 154], fill=(255, 255, 255))
    d.polygon([(120, 58), (202, 42), (202, 64), (120, 80)], fill=(255, 255, 255))
    write(img, "vk-music.webp")

    # VK Video
    img, d = canvas((38, 131, 237))
    d.rounded_rectangle([48, 70, 208, 186], radius=30, fill=(255, 255, 255))
    d.polygon([(100, 100), (100, 156), (160, 128)], fill=(38, 131, 237))
    write(img, "vk-video.webp")

    # YouTube if weak
    if (OUT / "youtube.webp").stat().st_size < 2000:
        img, d = canvas((255, 0, 0))
        d.rounded_rectangle([52, 78, 204, 178], radius=36, fill=(255, 255, 255))
        d.polygon([(108, 104), (108, 152), (158, 128)], fill=(255, 0, 0))
        # Better classic: red play on white? Actually YT is red bg white play
        img, d = canvas((255, 255, 255))
        d.rounded_rectangle([40, 78, 216, 178], radius=40, fill=(255, 0, 0))
        d.polygon([(108, 104), (108, 152), (162, 128)], fill=(255, 255, 255))
        write(img, "youtube.webp")

    # Yandex Music
    if (OUT / "yandex-music.webp").stat().st_size < 3000:
        img, d = canvas((255, 204, 0))
        # black note-ish circle mark
        d.ellipse([72, 72, 184, 184], fill=(0, 0, 0))
        d.ellipse([96, 96, 160, 160], fill=(255, 204, 0))
        d.ellipse([112, 112, 144, 144], fill=(0, 0, 0))
        write(img, "yandex-music.webp")

    # OK
    if (OUT / "ok.webp").stat().st_size < 3000:
        img, d = canvas((238, 130, 8))
        d.ellipse([78, 48, 178, 148], outline=(255, 255, 255), width=18)
        d.arc([64, 120, 192, 220], 200, 340, fill=(255, 255, 255), width=18)
        write(img, "ok.webp")

    # MAX
    img, d = canvas((92, 64, 214))
    center_text(d, "MAX", (255, 255, 255), 60, -4)
    d.polygon([(90, 88), (108, 114), (72, 114)], fill=(255, 204, 0))
    d.polygon([(180, 140), (208, 112), (208, 168)], fill=(255, 204, 0))
    write(img, "max.webp")

    # Rave
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        d.line(
            [(0, y), (SIZE, y)],
            fill=(int(255 - 100 * t), int(50 + 30 * t), int(160 + 60 * t), 255),
        )
    # mask to rounded
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=57, fill=255)
    rounded_img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    rounded_img.paste(img, mask=mask)
    d = ImageDraw.Draw(rounded_img)
    d.ellipse([74, 74, 182, 182], fill=(255, 255, 255))
    d.polygon([(112, 104), (112, 152), (158, 128)], fill=(220, 40, 140))
    write(rounded_img, "rave.webp")

    # Minecraft if weak
    if (OUT / "minecraft.webp").stat().st_size < 3000:
        img, d = canvas((93, 156, 62))
        # dirt/grass block vibe
        d.rectangle([48, 48, 208, 100], fill=(124, 180, 70))
        d.rectangle([48, 100, 208, 208], fill=(120, 85, 50))
        for x in range(48, 208, 40):
            d.line([(x, 100), (x, 208)], fill=(90, 60, 35), width=2)
        for y in range(100, 208, 40):
            d.line([(48, y), (208, y)], fill=(90, 60, 35), width=2)
        write(img, "minecraft.webp")

    # Null's Brawl
    img, d = canvas((20, 120, 220))
    d.ellipse([36, 36, 220, 220], fill=(255, 196, 0))
    d.regular_polygon((128, 120, 52), n_sides=5, rotation=90, fill=(20, 100, 200))
    center_text(d, "NB", (255, 255, 255), 40, 58)
    write(img, "nulls-brawl.webp")

    print("done")


if __name__ == "__main__":
    make_all()
