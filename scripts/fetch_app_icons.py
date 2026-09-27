"""Download real App Store / brand icons for the miniapp decoration grid."""
from __future__ import annotations

import io
import json
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)

# iTunes Search API — country RU for Russian apps
LOOKUPS: dict[str, dict] = {
    "tbank": {"term": "Т-Банк", "bundle": "com.idamob.tinkoff.android"},
    "alfabank": {"term": "Альфа-Банк", "bundle": "ru.alfabank.mobile.android"},
    "sberbank": {"term": "СберБанк", "bundle": "ru.sberbankmobile"},
    "youtube": {"term": "YouTube", "bundle": "com.google.ios.youtube"},
    "vk": {"term": "VK", "bundle": "com.vk.vkclient"},
    "vk-music": {"term": "VK Музыка", "bundle": "com.vk.music"},
    "vk-video": {"term": "VK Видео", "bundle": "com.vk.vkvideo"},
    "vtb": {"term": "ВТБ", "bundle": "ru.vtb24.mobilebanking.android"},
    "yandex-music": {"term": "Яндекс Музыка", "bundle": "ru.yandex.music"},
    "max": {"term": "MAX мессенджер", "artist": "VK"},
    "rave": {"term": "Rave", "bundle": "com.rave.android"},
    "ok": {"term": "Одноклассники", "bundle": "ru.ok.android"},
    "minecraft": {"term": "Minecraft", "bundle": "com.mojang.minecraftpe"},
    "nulls-brawl": {"term": "Null's Brawl", "media": "software"},
}

FALLBACK_URLS: dict[str, str] = {
    # Brand logo CDNs as last resort
    "tbank": "https://logo.clearbit.com/tbank.ru",
    "alfabank": "https://logo.clearbit.com/alfabank.ru",
    "sberbank": "https://logo.clearbit.com/sberbank.ru",
    "youtube": "https://logo.clearbit.com/youtube.com",
    "vk": "https://logo.clearbit.com/vk.com",
    "vtb": "https://logo.clearbit.com/vtb.ru",
    "yandex-music": "https://logo.clearbit.com/music.yandex.ru",
    "ok": "https://logo.clearbit.com/ok.ru",
    "minecraft": "https://logo.clearbit.com/minecraft.net",
}

CTX = ssl.create_default_context()


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; IconFetcher/1.0)"},
    )
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        return resp.read()


def itunes_artwork(term: str, bundle: str | None = None, artist: str | None = None) -> str | None:
    qs = urllib.parse.urlencode(
        {
            "term": term,
            "country": "ru",
            "entity": "software",
            "limit": 12,
        }
    )
    data = json.loads(fetch(f"https://itunes.apple.com/search?{qs}"))
    results = data.get("results") or []
    if not results:
        qs = urllib.parse.urlencode(
            {"term": term, "country": "us", "entity": "software", "limit": 12}
        )
        data = json.loads(fetch(f"https://itunes.apple.com/search?{qs}"))
        results = data.get("results") or []

    if bundle:
        for r in results:
            if r.get("bundleId") == bundle:
                return r.get("artworkUrl512") or r.get("artworkUrl100")
    if artist:
        for r in results:
            if artist.lower() in (r.get("artistName") or "").lower():
                return r.get("artworkUrl512") or r.get("artworkUrl100")
    if results:
        # Prefer exact-ish name match
        term_l = term.lower()
        for r in results:
            name = (r.get("trackName") or "").lower()
            if term_l.split()[0] in name:
                return r.get("artworkUrl512") or r.get("artworkUrl100")
        return results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
    return None


def to_squircle_webp(raw: bytes, path: Path, size: int = 256) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    # Keep full square — CSS already applies iOS squircle radius
    img.save(path, "WEBP", quality=92)


def main() -> None:
    for app_id, meta in LOOKUPS.items():
        out = OUT / f"{app_id}.webp"
        print(f"[{app_id}] ...", end=" ", flush=True)
        try:
            art = itunes_artwork(
                meta["term"],
                bundle=meta.get("bundle"),
                artist=meta.get("artist"),
            )
            if art:
                # Prefer higher res if available
                art = art.replace("512x512bb", "1024x1024bb")
                raw = fetch(art)
                to_squircle_webp(raw, out)
                print(f"App Store OK ({out.stat().st_size} bytes)")
                continue
        except Exception as e:
            print(f"itunes fail ({e})", end=" ")

        fb = FALLBACK_URLS.get(app_id)
        if fb:
            try:
                raw = fetch(fb)
                to_squircle_webp(raw, out)
                print(f"fallback OK ({out.stat().st_size} bytes)")
                continue
            except Exception as e:
                print(f"fallback fail ({e})")
        print("SKIPPED")


if __name__ == "__main__":
    main()
