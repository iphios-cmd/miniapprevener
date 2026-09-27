"""Fetch / generate reliable app icons into public/icons/*.webp"""
from __future__ import annotations

import io
import json
import ssl
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)
CTX = ssl.create_default_context()

# Official / known App Store IDs (still published)
APP_STORE_IDS: dict[str, int] = {
    "youtube": 544007664,
    "minecraft": 479516143,
    "vk": 564177498,
    "ok": 401271034,
    "yandex-music": 518133398,
    "tbank": 1360253417,
    "rave": 1129958305,
}

CDN: dict[str, list[str]] = {
    "sberbank": [
        "https://logo.clearbit.com/sber.ru",
        "https://logo.clearbit.com/sberbank.ru",
        "https://www.google.com/s2/favicons?domain=sberbank.ru&sz=128",
    ],
    "alfabank": [
        "https://logo.clearbit.com/alfabank.ru",
        "https://www.google.com/s2/favicons?domain=alfabank.ru&sz=128",
    ],
    "vtb": [
        "https://logo.clearbit.com/vtb.ru",
        "https://www.google.com/s2/favicons?domain=vtb.ru&sz=128",
    ],
    "vk-music": [
        "https://www.google.com/s2/favicons?domain=music.vk.com&sz=128",
    ],
    "vk-video": [
        "https://www.google.com/s2/favicons?domain=vkvideo.ru&sz=128",
        "https://logo.clearbit.com/vkvideo.ru",
    ],
    "max": [
        "https://logo.clearbit.com/max.ru",
        "https://www.google.com/s2/favicons?domain=max.ru&sz=128",
    ],
    "nulls-brawl": [
        "https://www.google.com/s2/favicons?domain=nulls-brawl.com&sz=128",
        "https://logo.clearbit.com/nullsbrawl.com",
    ],
}


def http_get(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 180:
        raise ValueError("payload too small")
    return data


def itunes_art(app_id: int) -> str | None:
    raw = http_get(f"https://itunes.apple.com/lookup?id={app_id}")
    results = json.loads(raw).get("results") or []
    if not results:
        return None
    art = results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
    if not art:
        return None
    return art.replace("512x512bb", "1024x1024bb")


def save_icon(raw: bytes, path: Path, size: int = 256) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = img.size
    if abs(w - h) > 2:
        side = max(w, h)
        canvas = Image.new("RGBA", (side, side), (255, 255, 255, 0))
        canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
        img = canvas
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(path, "WEBP", quality=93)


def font(size: int):
    for name in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, size: int, color: tuple[int, int, int]) -> None:
    r = int(size * 0.2237)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=color)


def draw_brand(app_id: str, path: Path, size: int = 256) -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if app_id == "sberbank":
        rounded(d, size, (21, 160, 56))
        # Sber checkmark stylized circle
        d.arc([52, 52, 204, 204], start=200, end=70, fill=(255, 255, 255), width=22)
        d.ellipse([150, 70, 186, 106], fill=(255, 255, 255))
    elif app_id == "alfabank":
        rounded(d, size, (239, 49, 36))
        d.polygon([(128, 40), (210, 210), (46, 210)], fill=(255, 255, 255))
        d.polygon([(128, 88), (176, 190), (80, 190)], fill=(239, 49, 36))
    elif app_id == "vtb":
        rounded(d, size, (0, 90, 170))
        f = font(72)
        # VTB wordmark
        bbox = d.textbbox((0, 0), "ВТБ", font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((size - tw) / 2, (size - th) / 2 - 6), "ВТБ", font=f, fill=(255, 255, 255))
    elif app_id == "vk-music":
        rounded(d, size, (252, 44, 56))
        d.ellipse([62, 148, 118, 204], fill=(255, 255, 255))
        d.ellipse([138, 128, 194, 184], fill=(255, 255, 255))
        d.rectangle([106, 64, 118, 170], fill=(255, 255, 255))
        d.rectangle([182, 48, 194, 150], fill=(255, 255, 255))
        d.polygon([(118, 64), (194, 48), (194, 68), (118, 84)], fill=(255, 255, 255))
    elif app_id == "vk-video":
        rounded(d, size, (38, 131, 237))
        d.rounded_rectangle([52, 72, 204, 184], radius=28, fill=(255, 255, 255))
        d.polygon([(104, 100), (104, 156), (160, 128)], fill=(38, 131, 237))
    elif app_id == "rave":
        for y in range(size):
            t = y / (size - 1)
            color = (
                int(255 * (1 - t) + 120 * t),
                int(60 * (1 - t) + 40 * t),
                int(140 * (1 - t) + 220 * t),
            )
            d.line([(0, y), (size, y)], fill=color + (255,))
        d.ellipse([70, 70, 186, 186], fill=(255, 255, 255))
        d.polygon([(108, 100), (108, 156), (158, 128)], fill=(200, 40, 160))
    elif app_id == "max":
        rounded(d, size, (92, 64, 214))
        f = font(64)
        bbox = d.textbbox((0, 0), "MAX", font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((size - tw) / 2, (size - th) / 2 - 8), "MAX", font=f, fill=(255, 255, 255))
        # accent triangles
        d.polygon([(96, 92), (112, 116), (80, 116)], fill=(255, 204, 0))
        d.polygon([(176, 140), (200, 116), (200, 164)], fill=(255, 204, 0))
    elif app_id == "nulls-brawl":
        rounded(d, size, (20, 120, 220))
        d.ellipse([40, 40, 216, 216], fill=(255, 196, 0))
        d.regular_polygon((128, 128, 58), n_sides=5, rotation=90, fill=(20, 120, 220))
        f = font(36)
        d.text((88, 176), "NB", font=f, fill=(255, 255, 255))
    else:
        rounded(d, size, (106, 165, 244))

    img.save(path, "WEBP", quality=93)


def try_cdn(app_id: str) -> bool:
    for url in CDN.get(app_id, []):
        try:
            raw = http_get(url)
            save_icon(raw, OUT / f"{app_id}.webp")
            return True
        except Exception:
            continue
    return False


def main() -> None:
    # Keep known-good apps from App Store
    for app_id, store_id in APP_STORE_IDS.items():
        print(f"[{app_id}] App Store...", end=" ", flush=True)
        try:
            art = itunes_art(store_id)
            if not art:
                raise ValueError("no artwork")
            save_icon(http_get(art), OUT / f"{app_id}.webp")
            print(f"OK ({(OUT / f'{app_id}.webp').stat().st_size})")
        except Exception as e:
            print(f"fail ({e})")
            if not try_cdn(app_id):
                draw_brand(app_id, OUT / f"{app_id}.webp")
                print(f"  drawn fallback")

    # Banks / special apps — CDN then draw
    for app_id in (
        "sberbank",
        "alfabank",
        "vtb",
        "vk-music",
        "vk-video",
        "max",
        "nulls-brawl",
    ):
        print(f"[{app_id}] CDN/draw...", end=" ", flush=True)
        if try_cdn(app_id):
            print(f"OK ({(OUT / f'{app_id}.webp').stat().st_size})")
        else:
            draw_brand(app_id, OUT / f"{app_id}.webp")
            print(f"drawn ({(OUT / f'{app_id}.webp').stat().st_size})")


if __name__ == "__main__":
    main()
