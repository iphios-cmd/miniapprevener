"""Fix wrong icons with precise public sources."""
from __future__ import annotations

import io
import json
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("public/icons")
CTX = ssl.create_default_context()
SIZE = 256


def http(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; IconBot/1.0)",
            "Accept": "image/*,*/*",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        data = r.read()
    if len(data) < 400:
        raise ValueError(f"small {len(data)} for {url}")
    return data


def save(raw: bytes, name: str) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = img.size
    if abs(w - h) > 2:
        side = max(w, h)
        c = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        c.paste(img, ((side - w) // 2, (side - h) // 2), img)
        img = c
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    path = OUT / name
    img.save(path, "WEBP", quality=95)
    print(f"OK {name} ({path.stat().st_size})")


def save_on_bg(raw: bytes, name: str, bg: tuple[int, int, int], pad: float = 0.18) -> None:
    logo = Image.open(io.BytesIO(raw)).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    max_side = int(SIZE * (1 - 2 * pad))
    logo.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=57, fill=bg)
    x = (SIZE - logo.size[0]) // 2
    y = (SIZE - logo.size[1]) // 2
    canvas.paste(logo, (x, y), logo)
    path = OUT / name
    canvas.save(path, "WEBP", quality=95)
    print(f"OK {name} on-bg ({path.stat().st_size})")


def itunes(app_id: int, country: str = "us") -> bytes:
    meta = json.loads(http(f"https://itunes.apple.com/lookup?id={app_id}&country={country}"))
    results = meta.get("results") or []
    if not results:
        raise ValueError(f"no itunes results {app_id}")
    art = results[0].get("artworkUrl512")
    print(f"  itunes {app_id} -> {results[0].get('trackName')}")
    art = art.replace("512x512bb", "1024x1024bb")
    return http(art)


# Precise known-good sources
TARGETS = {
    # Official YouTube (already good) keep
    "youtube": lambda: itunes(544007664),
    # Minecraft Pocket Edition
    "minecraft": lambda: itunes(479516143),
    # VK iOS
    "vk": lambda: itunes(564177498),
    # OK
    "ok": lambda: itunes(401271034),
    # Yandex Music exact id
    "yandex-music": lambda: itunes(518133398),
    # Rave watch party - try multiple
    "rave": lambda: itunes(1129958305),
}

# Wikimedia / brand CDN URLs (allowed sizes)
WIKI = {
    "sberbank": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Sberbank_logo_2020.svg/200px-Sberbank_logo_2020.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Sberbank_logo_2020.svg/120px-Sberbank_logo_2020.svg.png",
    ],
    "alfabank": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Alfa-Bank_logo.svg/200px-Alfa-Bank_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Alfa-Bank_logo.svg/120px-Alfa-Bank_logo.svg.png",
    ],
    "vtb": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/VTB_logo.svg/200px-VTB_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/VTB_Bank_logo.svg/200px-VTB_Bank_logo.svg.png",
    ],
    "vk": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VK_Compact_Logo_%282021-present%29.svg/200px-VK_Compact_Logo_%282021-present%29.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/VK.com-logo.svg/200px-VK.com-logo.svg.png",
    ],
    "ok": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/OK.ru_logo.svg/200px-OK.ru_logo.svg.png",
    ],
    "youtube": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/200px-YouTube_full-color_icon_%282017%29.svg.png",
    ],
}

BG = {
    "sberbank": (255, 255, 255),
    "alfabank": (239, 49, 36),
    "vtb": (0, 90, 170),
    "vk": (0, 119, 255),
    "ok": (238, 130, 8),
    "youtube": (255, 255, 255),
}

# Softpedia / alternative direct PNGs and apple-touch-icons
DIRECT = {
    "tbank": [
        "https://www.tbank.ru/apple-touch-icon.png",
        "https://cdn.tbank.ru/static/pages/files/apple-touch-icon.png",
        "https://www.tinkoff.ru/apple-touch-icon.png",
    ],
    "max": [
        "https://max.ru/apple-touch-icon.png",
        "https://web.max.ru/apple-touch-icon.png",
    ],
    "vk-music": [
        "https://music.vk.com/apple-touch-icon.png",
        "https://vk.com/images/icons/pwa/apple/default.png",
    ],
    "vk-video": [
        "https://vkvideo.ru/apple-touch-icon.png",
        "https://vk.com/images/icons/pwa/apple/default.png",
    ],
    "yandex-music": [
        "https://music.yandex.ru/apple-touch-icon.png",
        "https://yastatic.net/s3/doc-binary/src/frontend/music/apple-touch-icon-180.png",
    ],
    "rave": [
        "https://rave.io/apple-touch-icon.png",
        "https://www.rave.io/apple-touch-icon.png",
    ],
    "nulls-brawl": [
        "https://nulls-brawl.com/apple-touch-icon.png",
        "https://nullsbrawl.com/apple-touch-icon.png",
        "https://nulls-brawl.com/favicon-196x196.png",
    ],
    "alfabank": [
        "https://alfabank.ru/apple-touch-icon.png",
        "https://alfabank.ru/favicon-196x196.png",
    ],
    "vtb": [
        "https://www.vtb.ru/apple-touch-icon.png",
        "https://online.vtb.ru/apple-touch-icon.png",
    ],
    "sberbank": [
        "https://www.sberbank.ru/apple-touch-icon.png",
        "https://www.sber.ru/apple-touch-icon.png",
    ],
}


def try_list(urls: list[str]) -> bytes | None:
    for u in urls:
        try:
            return http(u)
        except Exception as e:
            print(f"  fail {u[:70]} ({e})")
    return None


def main() -> None:
    # 1) Exact iTunes where IDs are reliable
    for name, fn in TARGETS.items():
        print(f"[{name}] itunes")
        try:
            save(fn(), f"{name}.webp")
        except Exception as e:
            print(f"  itunes fail: {e}")

    # 2) Wiki logos on brand bg
    for name, urls in WIKI.items():
        print(f"[{name}] wiki")
        raw = try_list(urls)
        if raw:
            bg = BG.get(name, (255, 255, 255))
            # For logos that already include color, white bg; for white logos use brand bg
            if name in ("vk", "ok", "alfabank", "vtb"):
                save_on_bg(raw, f"{name}.webp", bg, pad=0.2)
            else:
                save_on_bg(raw, f"{name}.webp", bg, pad=0.12)
        else:
            print("  wiki miss")

    # 3) Direct apple-touch / site icons
    for name, urls in DIRECT.items():
        print(f"[{name}] direct")
        raw = try_list(urls)
        if raw:
            save(raw, f"{name}.webp")
        else:
            print("  direct miss")

    print("done")


if __name__ == "__main__":
    main()
