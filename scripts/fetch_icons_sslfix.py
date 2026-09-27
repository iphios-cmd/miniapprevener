"""Fetch real icons with SSL workarounds + public CDNs."""
from __future__ import annotations

import io
import json
import ssl
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 256
CTX = ssl._create_unverified_context()


def http(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "image/*,*/*"},
    )
    with urllib.request.urlopen(req, context=CTX, timeout=35) as r:
        data = r.read()
    if len(data) < 300:
        raise ValueError(f"small {len(data)}")
    return data


def curl(url: str) -> bytes:
    p = subprocess.run(
        ["curl", "-kL", "--max-time", "35", "-A", "Mozilla/5.0", url],
        capture_output=True,
    )
    if p.returncode != 0 or len(p.stdout) < 300:
        raise ValueError(f"curl fail {url} ({len(p.stdout)})")
    return p.stdout


def get(url: str) -> bytes:
    try:
        data = http(url)
    except Exception:
        data = curl(url)
    # Must be an image
    try:
        Image.open(io.BytesIO(data)).verify()
    except Exception as e:
        raise ValueError(f"not an image ({e})") from e
    return data


def save_square(raw: bytes, name: str) -> None:
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
    print(f"  saved {name} ({path.stat().st_size})")


def save_logo_on_bg(raw: bytes, name: str, bg: tuple[int, int, int], pad: float = 0.18) -> None:
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
    print(f"  saved {name} ({path.stat().st_size})")


def itunes(app_id: int) -> bytes:
    for country in ("us", "ru", "gb"):
        meta = json.loads(get(f"https://itunes.apple.com/lookup?id={app_id}&country={country}"))
        results = meta.get("results") or []
        if not results:
            continue
        print(f"  itunes -> {results[0].get('trackName')}")
        art = results[0]["artworkUrl512"].replace("512x512bb", "1024x1024bb")
        return get(art)
    raise ValueError(f"no itunes {app_id}")


def iconify_png(collection: str, name: str, color: str | None = None) -> bytes:
    # SVG via iconify, rasterize with cairosvg not available — use png endpoint if exists
    # Fallback: download SVG and tell pillow won't work. Use jsdelivr png from simple-icons? no png.
    # Use google favicon / duckduckgo icons which are real brand marks.
    raise NotImplementedError


# Sources proven to work for brand marks
JOBS: list[tuple[str, list[str], tuple[int, int, int] | None]] = [
    # name, urls, optional bg (if logo needs background)
    (
        "youtube",
        [
            "https://www.youtube.com/s/desktop/12d6b45c/img/favicon_144x144.png",
            "https://www.gstatic.com/youtube/img/branding/favicon/favicon_144x144.png",
        ],
        None,
    ),
    (
        "vk",
        [
            "https://sun9-80.userapi.com/s/v1/ig2/placeholder",  # may fail
            "https://vk.com/images/icons/pwa/apple/default.png",
            "https://vk.com/images/icons/favicons/fav_vk_2x.png",
        ],
        (0, 119, 255),
    ),
    (
        "ok",
        [
            "https://ok.ru/res/i/pwa/apple-touch-icon.png",
            "https://ok.ru/apple-touch-icon.png",
        ],
        None,
    ),
    (
        "yandex-music",
        [
            "https://music.yandex.ru/apple-touch-icon.png",
            "https://yastatic.net/s3/doc-binary/src/frontend/music/apple-touch-icon-180.png",
            "https://yastatic.net/iconostasis/_/8b0d55c5d5a8c0b5c5c5c5c5c5c5c5c5/music.png",
        ],
        None,
    ),
    (
        "max",
        [
            "https://max.ru/apple-touch-icon.png",
            "https://web.max.ru/apple-touch-icon.png",
        ],
        None,
    ),
    (
        "tbank",
        [
            "https://www.tbank.ru/favicon-196x196.png",
            "https://cdn.tbank.ru/static/pages/files/favicon-196x196.png",
            "https://www.tbank.ru/apple-touch-icon.png",
            "https://www.tinkoff.ru/apple-touch-icon.png",
        ],
        None,
    ),
    (
        "alfabank",
        [
            "https://alfabank.ru/apple-touch-icon.png",
            "https://alfabank.ru/favicon-196x196.png",
            "https://alfabank.servicecdn.ru/icons/apple-touch-icon.png",
        ],
        None,
    ),
    (
        "sberbank",
        [
            "https://www.sberbank.com/apple-touch-icon.png",
            "https://www.sberbank.ru/apple-touch-icon.png",
            "https://sberbank.ru/common/img/apple-touch-icon.png",
        ],
        None,
    ),
    (
        "vtb",
        [
            "https://www.vtb.ru/apple-touch-icon.png",
            "https://www.vtb.ru/favicon-196x196.png",
            "https://online.vtb.ru/favicon.ico",
        ],
        None,
    ),
    (
        "minecraft",
        [
            # App Store
        ],
        None,
    ),
    (
        "rave",
        [
            "https://rave.io/img/favicon.png",
            "https://cdn.rave.io/favicon-196x196.png",
            "https://static.rave.io/favicon.png",
        ],
        None,
    ),
    (
        "vk-music",
        [
            "https://vk.com/images/icons/pwa/apple/default.png",
        ],
        (252, 44, 56),
    ),
    (
        "vk-video",
        [
            "https://vk.com/images/icons/pwa/apple/default.png",
        ],
        (38, 131, 237),
    ),
    (
        "nulls-brawl",
        [
            "https://nulls-brawl.com/apple-touch-icon.png",
            "https://nullsbrawl.com/apple-touch-icon.png",
            "https://nulls-brawl.com/favicon-196x196.png",
        ],
        None,
    ),
]


def main() -> None:
    # Reliable App Store icons first
    store = {
        "youtube": 544007664,
        "minecraft": 479516143,
    }
    for name, aid in store.items():
        print(f"[{name}] store")
        try:
            save_square(itunes(aid), f"{name}.webp")
        except Exception as e:
            print(f"  fail {e}")

    for name, urls, bg in JOBS:
        if name in store:
            continue
        print(f"[{name}]")
        raw = None
        for u in urls:
            try:
                raw = get(u)
                print(f"  got {u[:70]}")
                break
            except Exception as e:
                print(f"  miss {e}")
        if not raw:
            print("  FAIL")
            continue
        if bg:
            save_logo_on_bg(raw, f"{name}.webp", bg)
        else:
            save_square(raw, f"{name}.webp")

    # Extra: duckduckgo icons (real favicons, often decent)
    ddg = {
        "sberbank": "sberbank.ru",
        "alfabank": "alfabank.ru",
        "vtb": "vtb.ru",
        "tbank": "tbank.ru",
        "rave": "rave.io",
        "vk": "vk.com",
    }
    for name, host in ddg.items():
        path = OUT / f"{name}.webp"
        # refresh weak ones (< 4kb often wrong/placeholder)
        if path.exists() and path.stat().st_size > 5000 and name != "alfabank":
            continue
        print(f"[{name}] ddg/iconhorse")
        for u in (
            f"https://icons.duckduckgo.com/ip3/{host}.ico",
            f"https://icon.horse/icon/{host}",
            f"https://www.google.com/s2/favicons?domain={host}&sz=128",
        ):
            try:
                raw = get(u)
                # put on brand bg if needed
                brand_bg = {
                    "sberbank": (21, 160, 56),
                    "alfabank": (239, 49, 36),
                    "vtb": (0, 90, 170),
                    "tbank": (255, 221, 45),
                    "rave": (120, 40, 180),
                    "vk": (0, 119, 255),
                }.get(name)
                if brand_bg and Image.open(io.BytesIO(raw)).size[0] < 180:
                    save_logo_on_bg(raw, f"{name}.webp", brand_bg, pad=0.22)
                else:
                    save_square(raw, f"{name}.webp")
                break
            except Exception as e:
                print(f"  miss {e}")

    print("\nFinal sizes:")
    for p in sorted(OUT.glob("*.webp")):
        print(f"  {p.name:22} {p.stat().st_size:7}")


if __name__ == "__main__":
    main()
