"""Scrape public icon hosts and download real app icons."""
from __future__ import annotations

import io
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)
CTX = ssl.create_default_context()
SIZE = 256

PACKAGES = {
    "sberbank": "ru.sberbankmobile",
    "alfabank": "ru.alfabank.mobile.android",
    "tbank": "com.idamob.tinkoff.android",
    "vtb": "ru.vtb24.mobilebanking.android",
    "vk": "com.vkontakte.android",
    "ok": "ru.ok.android",
    "youtube": "com.google.android.youtube",
    "yandex-music": "ru.yandex.music",
    "minecraft": "com.mojang.minecraftpe",
    "max": "ru.oneme.app",
    "rave": "com.rave.app",
    "vk-music": "com.vk.music",
    "vk-video": "com.vk.vkvideo",
    "nulls-brawl": "com.nulls.brawl",
}

ITUNES = {
    "youtube": 544007664,
    "minecraft": 479516143,
    "vk": 564177498,
    "ok": 401271034,
    "yandex-music": 518133398,
    "tbank": 1360253417,
    "rave": 1129958305,
}

EXTRA_URLS = {
    "youtube": [
        "https://www.youtube.com/s/desktop/12d6b45c/img/favicon_144x144.png",
        "https://www.gstatic.com/youtube/img/branding/favicon/favicon_144x144.png",
    ],
    "vk": [
        "https://sun6-22.userapi.com/s/v1/if1/placeholder",
    ],
}


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 500:
        raise ValueError(f"too small {len(data)}")
    return data


def save_webp(raw: bytes, name: str) -> Path:
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = img.size
    if abs(w - h) > 2:
        side = max(w, h)
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
        img = canvas
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    path = OUT / name
    img.save(path, "WEBP", quality=95)
    return path


def itunes_icon(app_id: int) -> bytes | None:
    for country in ("us", "ru", "gb"):
        try:
            meta = json.loads(get(f"https://itunes.apple.com/lookup?id={app_id}&country={country}"))
            results = meta.get("results") or []
            if not results:
                continue
            art = results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
            if not art:
                continue
            art = art.replace("512x512bb", "1024x1024bb")
            return get(art)
        except Exception:
            continue
    return None


def iconpusher_icon(package: str) -> bytes | None:
    url = f"https://iconpusher.com/package/{package}"
    try:
        html = get(url).decode("utf-8", "ignore")
    except Exception as e:
        print(f"    iconpusher page fail: {e}")
        return None

    # Common patterns on iconpusher
    candidates = []
    candidates += re.findall(r'https://[^"\']+?\.(?:png|webp|jpg|jpeg)', html, re.I)
    candidates += re.findall(r'src="([^"]+)"', html)
    candidates += re.findall(r'href="([^"]+\.(?:png|webp|jpg))"', html, re.I)

    # Relative downloads
    for m in re.findall(r'href="(/[^"]+)"', html):
        if "download" in m or m.endswith((".png", ".webp")):
            candidates.append("https://iconpusher.com" + m)

    # Dedup keep order
    seen = set()
    uniq = []
    for c in candidates:
        if c.startswith("//"):
            c = "https:" + c
        if not c.startswith("http"):
            continue
        if c in seen:
            continue
        seen.add(c)
        uniq.append(c)

    for c in uniq:
        low = c.lower()
        if any(x in low for x in ("logo", "avatar", "sprite", "flag")):
            continue
        try:
            raw = get(c)
            # Heuristic: must look like an image large enough
            Image.open(io.BytesIO(raw)).verify()
            return get(c)  # re-fetch after verify consumed? better reopen
        except Exception:
            continue
    return None


def iconpusher_icon_fixed(package: str) -> bytes | None:
    url = f"https://iconpusher.com/package/{package}"
    try:
        html = get(url).decode("utf-8", "ignore")
    except Exception as e:
        print(f"    iconpusher page fail: {e}")
        return None

    candidates = []
    candidates += re.findall(r'https://[^"\']+?\.(?:png|webp|jpg|jpeg)', html, re.I)
    candidates += re.findall(r'src="([^"]+)"', html)
    candidates += re.findall(r'href="([^"]+\.(?:png|webp|jpg))"', html, re.I)
    for m in re.findall(r'href="(/[^"]+)"', html):
        if "download" in m or m.endswith((".png", ".webp")):
            candidates.append("https://iconpusher.com" + m)

    seen = set()
    for c in candidates:
        if c.startswith("//"):
            c = "https:" + c
        if not c.startswith("http") or c in seen:
            continue
        seen.add(c)
        try:
            raw = get(c)
            img = Image.open(io.BytesIO(raw))
            img.verify()
            # fetch again for actual pixels
            raw2 = get(c)
            w, h = Image.open(io.BytesIO(raw2)).size
            if min(w, h) < 48:
                continue
            return raw2
        except Exception:
            continue
    return None


def play_store_icon(package: str) -> bytes | None:
    url = f"https://play.google.com/store/apps/details?id={package}&hl=en&gl=us"
    try:
        html = get(url).decode("utf-8", "ignore")
    except Exception as e:
        print(f"    play fail: {e}")
        return None

    # googleusercontent icons
    matches = re.findall(
        r'(https://play-lh\.googleusercontent\.com/[^"\'=\s]+)',
        html,
    )
    # Prefer larger (=s512 / =w512)
    ranked = sorted(
        set(matches),
        key=lambda u: (("=s512" in u or "=w512" in u or "=s256" in u), len(u)),
        reverse=True,
    )
    for m in ranked[:12]:
        # Normalize size
        u = re.sub(r"=s\d+.*$", "=s512-rw", m)
        u = re.sub(r"=w\d+.*$", "=s512-rw", u)
        try:
            return get(u)
        except Exception:
            try:
                return get(m)
            except Exception:
                continue
    return None


def apkpure_icon(package: str) -> bytes | None:
    # APKPure sometimes hosts icons
    url = f"https://apkpure.com/search?q={urllib.parse.quote(package)}"
    try:
        html = get(url).decode("utf-8", "ignore")
    except Exception:
        return None
    imgs = re.findall(r'(https://image\.winudf\.com/[^"\']+)', html)
    for u in imgs[:5]:
        try:
            return get(u)
        except Exception:
            continue
    return None


def main() -> None:
    for app_id, package in PACKAGES.items():
        print(f"[{app_id}] {package}")
        raw = None
        how = None

        # 1) Google Play (best for Android store icons)
        raw = play_store_icon(package)
        if raw:
            how = "play"

        # 2) App Store
        if not raw and app_id in ITUNES:
            raw = itunes_icon(ITUNES[app_id])
            if raw:
                how = "itunes"

        # 3) Iconpusher
        if not raw:
            raw = iconpusher_icon_fixed(package)
            if raw:
                how = "iconpusher"

        # 4) APKPure
        if not raw:
            raw = apkpure_icon(package)
            if raw:
                how = "apkpure"

        # 5) Extra direct
        if not raw:
            for u in EXTRA_URLS.get(app_id, []):
                try:
                    raw = get(u)
                    how = "direct"
                    break
                except Exception:
                    continue

        if raw:
            path = save_webp(raw, f"{app_id}.webp")
            print(f"  OK {how} -> {path.name} ({path.stat().st_size})")
        else:
            print("  FAIL")
        time.sleep(0.4)

    print("\nFiles:")
    for p in sorted(OUT.glob("*.webp")):
        print(f"  {p.name:22} {p.stat().st_size:7}")


if __name__ == "__main__":
    main()
