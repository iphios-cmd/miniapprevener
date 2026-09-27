"""Download REAL app icons (App Store artwork / Play og:image / icon hosts)."""
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

# Known good App Store IDs + search fallbacks
APPS: dict[str, dict] = {
    "youtube": {
        "itunes": [544007664],
        "play": "com.google.android.youtube",
        "search": ["YouTube"],
    },
    "minecraft": {
        "itunes": [479516143],
        "play": "com.mojang.minecraftpe",
        "search": ["Minecraft"],
    },
    "vk": {
        "itunes": [564177498],
        "play": "com.vkontakte.android",
        "search": ["VK"],
        "hosts": ["vk.com"],
    },
    "ok": {
        "itunes": [401271034],
        "play": "ru.ok.android",
        "search": ["Одноклассники", "OK.ru"],
        "hosts": ["ok.ru"],
    },
    "yandex-music": {
        "itunes": [518133398],
        "play": "ru.yandex.music",
        "search": ["Yandex Music", "Яндекс Музыка"],
        "hosts": ["music.yandex.ru"],
    },
    "tbank": {
        "itunes": [1360253417, 1477594869],
        "play": "com.idamob.tinkoff.android",
        "search": ["T-Bank", "Tinkoff"],
        "hosts": ["tbank.ru", "tinkoff.ru"],
        "iconpusher": "com.idamob.tinkoff.android",
    },
    "alfabank": {
        "itunes": [1217378858, 946069284],
        "play": "ru.alfabank.mobile.android",
        "search": ["Alfa-Bank", "Альфа-Банк"],
        "hosts": ["alfabank.ru"],
        "iconpusher": "ru.alfabank.mobile.android",
    },
    "sberbank": {
        "itunes": [492394852, 1361463185],
        "play": "ru.sberbankmobile",
        "search": ["Sberbank Online", "СберБанк"],
        "hosts": ["sberbank.ru", "sber.ru"],
        "iconpusher": "ru.sberbankmobile",
    },
    "vtb": {
        "itunes": [585408566],
        "play": "ru.vtb24.mobilebanking.android",
        "search": ["VTB Online", "ВТБ"],
        "hosts": ["vtb.ru"],
        "iconpusher": "ru.vtb24.mobilebanking.android",
    },
    "max": {
        "itunes": [6738278395, 6474564277],
        "play": "ru.oneme.app",
        "search": ["MAX"],
        "hosts": ["max.ru"],
    },
    "rave": {
        "itunes": [1129958305, 1451531884],
        "play": "live.rave.app",
        "search": ["Rave Watch Party", "Rave"],
        "hosts": ["rave.io"],
    },
    "vk-music": {
        "itunes": [],
        "play": "com.vk.music",
        "search": ["VK Music", "VK Музыка"],
        "hosts": ["music.vk.com"],
    },
    "vk-video": {
        "itunes": [],
        "play": "com.vk.vkvideo",
        "search": ["VK Video", "VK Видео"],
        "hosts": ["vkvideo.ru"],
    },
    "nulls-brawl": {
        "itunes": [],
        "play": "",
        "search": ["Null's Brawl", "Brawl Stars"],
        "hosts": ["nulls-brawl.com", "nullsbrawl.com"],
    },
}


def http(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
            ),
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
        data = r.read()
    if len(data) < 800:
        raise ValueError(f"small {len(data)}")
    return data


def looks_like_icon(raw: bytes) -> bool:
    try:
        img = Image.open(io.BytesIO(raw))
        w, h = img.size
        if min(w, h) < 64:
            return False
        # Reject very wide screenshots
        ratio = max(w, h) / max(1, min(w, h))
        if ratio > 1.35:
            return False
        return True
    except Exception:
        return False


def save(raw: bytes, name: str) -> Path:
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


def itunes_by_id(app_id: int) -> bytes | None:
    for country in ("us", "ru", "gb", "de"):
        try:
            meta = json.loads(http(f"https://itunes.apple.com/lookup?id={app_id}&country={country}"))
            results = meta.get("results") or []
            if not results:
                continue
            art = results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
            if not art:
                continue
            art = art.replace("512x512bb", "1024x1024bb")
            raw = http(art)
            if looks_like_icon(raw):
                return raw
        except Exception:
            continue
    return None


def itunes_search(term: str) -> bytes | None:
    for country in ("us", "ru"):
        qs = urllib.parse.urlencode(
            {"term": term, "country": country, "entity": "software", "limit": 10}
        )
        try:
            data = json.loads(http(f"https://itunes.apple.com/search?{qs}"))
        except Exception:
            continue
        term_l = term.lower()
        ranked = []
        for r in data.get("results") or []:
            name = (r.get("trackName") or "").lower()
            score = 0
            if term_l in name:
                score += 5
            for part in term_l.split():
                if part in name:
                    score += 1
            art = r.get("artworkUrl512") or r.get("artworkUrl100")
            if art:
                ranked.append((score, art, name))
        ranked.sort(reverse=True)
        for score, art, name in ranked[:5]:
            if score < 1:
                continue
            try:
                art = art.replace("512x512bb", "1024x1024bb")
                raw = http(art)
                if looks_like_icon(raw):
                    return raw
            except Exception:
                continue
    return None


def play_og_image(package: str) -> bytes | None:
    if not package:
        return None
    url = f"https://play.google.com/store/apps/details?id={package}&hl=en&gl=us"
    try:
        html = http(url).decode("utf-8", "ignore")
    except Exception as e:
        print(f"    play page: {e}")
        return None

    # Prefer og:image (usually the icon)
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            html,
            re.I,
        )
    candidates = []
    if m:
        candidates.append(m.group(1))

    # Also try itemprop=image
    candidates += re.findall(
        r'itemprop=["\']image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I
    )
    candidates += re.findall(
        r'content=["\'](https://play-lh\.googleusercontent\.com/[^"\']+)["\'][^>]+itemprop=["\']image["\']',
        html,
        re.I,
    )

    for c in candidates:
        c = c.replace("&amp;", "&")
        # bump size
        c2 = re.sub(r"=w\d+.*$", "=s512-rw", c)
        for u in (c2, c):
            try:
                raw = http(u)
                if looks_like_icon(raw):
                    return raw
            except Exception:
                continue
    return None


def icon_horse(host: str) -> bytes | None:
    try:
        raw = http(f"https://icon.horse/icon/{host}")
        if looks_like_icon(raw):
            return raw
    except Exception:
        pass
    try:
        raw = http(f"https://www.google.com/s2/favicons?domain={host}&sz=128")
        if looks_like_icon(raw):
            return raw
    except Exception:
        pass
    return None


def iconpusher(package: str) -> bytes | None:
    url = f"https://iconpusher.com/package/{package}"
    try:
        html = http(url).decode("utf-8", "ignore")
    except Exception as e:
        print(f"    iconpusher: {e}")
        return None

    # Direct image links often under /icons/ or cdn
    urls = re.findall(r'https://[^"\']+\.(?:png|webp|jpg)', html, re.I)
    urls += ["https://iconpusher.com" + m for m in re.findall(r'href="(/[^"]*download[^"]*)"', html)]
    urls += ["https://iconpusher.com" + m for m in re.findall(r'src="(/[^"]+\.png)"', html)]

    for u in urls:
        try:
            raw = http(u)
            if looks_like_icon(raw):
                return raw
        except Exception:
            continue
    return None


def main() -> None:
    for app_id, cfg in APPS.items():
        print(f"[{app_id}]")
        raw = None
        how = None

        for itunes_id in cfg.get("itunes") or []:
            raw = itunes_by_id(itunes_id)
            if raw:
                how = f"itunes:{itunes_id}"
                break

        if not raw:
            for term in cfg.get("search") or []:
                raw = itunes_search(term)
                if raw:
                    how = f"search:{term}"
                    break

        if not raw:
            raw = play_og_image(cfg.get("play") or "")
            if raw:
                how = "play-og"

        if not raw and cfg.get("iconpusher"):
            raw = iconpusher(cfg["iconpusher"])
            if raw:
                how = "iconpusher"

        if not raw:
            for host in cfg.get("hosts") or []:
                raw = icon_horse(host)
                if raw:
                    how = f"host:{host}"
                    break

        if raw:
            path = save(raw, f"{app_id}.webp")
            print(f"  OK {how} -> {path.stat().st_size} bytes")
        else:
            print("  FAIL")
        time.sleep(0.25)

    print("\nDone.")


if __name__ == "__main__":
    main()
