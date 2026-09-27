"""Download real app icons from public sources into public/icons/."""
from __future__ import annotations

import io
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path("public/icons")
OUT.mkdir(parents=True, exist_ok=True)
CTX = ssl.create_default_context()
SIZE = 256

# Multiple public sources per app (tried in order)
SOURCES: dict[str, list[str]] = {
    "youtube": [
        "https://www.youtube.com/s/desktop/12d6b45c/img/favicon_144x144.png",
        "https://www.gstatic.com/youtube/img/branding/youtubelogo/svg/youtubelogo.svg",
        "https://ssl.gstatic.com/gb/images/a/1715adbf59.png",
        "https://icon.horse/icon/youtube.com",
        "https://www.google.com/s2/favicons?domain=youtube.com&sz=128",
    ],
    "vk": [
        "https://vk.com/images/icons/favicons/fav_vk.ico",
        "https://vk.com/images/icons/pwa/apple/default.png",
        "https://sun9-22.userapi.com/impf/c848416/v848416262/1d2a66/placeholder.png",
        "https://icon.horse/icon/vk.com",
        "https://www.google.com/s2/favicons?domain=vk.com&sz=128",
    ],
    "ok": [
        "https://ok.ru/favicon.ico",
        "https://icon.horse/icon/ok.ru",
        "https://www.google.com/s2/favicons?domain=ok.ru&sz=128",
    ],
    "tbank": [
        "https://cdn.tbank.ru/static/pages/files/favicon.ico",
        "https://www.tbank.ru/favicon.ico",
        "https://icon.horse/icon/tbank.ru",
        "https://www.google.com/s2/favicons?domain=tbank.ru&sz=128",
        "https://www.google.com/s2/favicons?domain=tinkoff.ru&sz=128",
    ],
    "alfabank": [
        "https://alfabank.ru/favicon.ico",
        "https://icon.horse/icon/alfabank.ru",
        "https://www.google.com/s2/favicons?domain=alfabank.ru&sz=128",
    ],
    "sberbank": [
        "https://www.sberbank.ru/portalserver/static/templates/%5BBBHOST%5D/Master%20page.default/favicon.ico",
        "https://www.sberbank.com/favicon.ico",
        "https://icon.horse/icon/sberbank.ru",
        "https://www.google.com/s2/favicons?domain=sberbank.ru&sz=128",
        "https://www.google.com/s2/favicons?domain=sber.ru&sz=128",
    ],
    "vtb": [
        "https://www.vtb.ru/favicon.ico",
        "https://online.vtb.ru/favicon.ico",
        "https://icon.horse/icon/vtb.ru",
        "https://www.google.com/s2/favicons?domain=vtb.ru&sz=128",
    ],
    "yandex-music": [
        "https://music.yandex.ru/favicon.ico",
        "https://yastatic.net/s3/doc-binary/freeze/ru/music/apple-touch-icon-180.png",
        "https://icon.horse/icon/music.yandex.ru",
        "https://www.google.com/s2/favicons?domain=music.yandex.ru&sz=128",
    ],
    "vk-music": [
        "https://icon.horse/icon/music.vk.com",
        "https://www.google.com/s2/favicons?domain=vk.com&sz=128",
    ],
    "vk-video": [
        "https://icon.horse/icon/vkvideo.ru",
        "https://www.google.com/s2/favicons?domain=vkvideo.ru&sz=128",
    ],
    "max": [
        "https://max.ru/favicon.ico",
        "https://icon.horse/icon/max.ru",
        "https://www.google.com/s2/favicons?domain=max.ru&sz=128",
    ],
    "rave": [
        "https://rave.io/favicon.ico",
        "https://icon.horse/icon/rave.io",
        "https://www.google.com/s2/favicons?domain=rave.io&sz=128",
    ],
    "minecraft": [
        "https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon.ico",
        "https://icon.horse/icon/minecraft.net",
        "https://www.google.com/s2/favicons?domain=minecraft.net&sz=128",
    ],
    "nulls-brawl": [
        "https://nulls-brawl.com/favicon.ico",
        "https://nullsbrawl.com/favicon.ico",
        "https://icon.horse/icon/nulls-brawl.com",
        "https://www.google.com/s2/favicons?domain=nulls-brawl.com&sz=128",
    ],
}

# Better: iTunes lookup by numeric id (public Apple CDN artwork)
ITUNES_IDS: dict[str, list[int]] = {
    "youtube": [544007664],
    "minecraft": [479516143],
    "vk": [564177498],
    "ok": [401271034],
    "yandex-music": [518133398],
    "tbank": [1360253417, 1477594869],
    "alfabank": [1217378858, 946069284],
    "sberbank": [492394852, 1361463185],
    "vtb": [585408566, 1537860678],
    "rave": [1129958305, 1451531884],
    "max": [6474564277, 6738278395],
}


def fetch(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 400:
        raise ValueError(f"too small ({len(data)})")
    return data


def itunes_artwork(app_id: int) -> str | None:
    url = f"https://itunes.apple.com/lookup?id={app_id}&country=ru"
    try:
        raw = fetch(url)
    except Exception:
        url = f"https://itunes.apple.com/lookup?id={app_id}&country=us"
        raw = fetch(url)
    results = json.loads(raw).get("results") or []
    if not results:
        return None
    art = results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
    if not art:
        return None
    return art.replace("512x512bb", "1024x1024bb")


def itunes_search(term: str, country: str = "ru") -> str | None:
    qs = urllib.parse.urlencode(
        {"term": term, "country": country, "entity": "software", "limit": 8}
    )
    data = json.loads(fetch(f"https://itunes.apple.com/search?{qs}"))
    results = data.get("results") or []
    term_l = term.lower()
    for r in results:
        name = (r.get("trackName") or "").lower()
        if any(p in name for p in term_l.split()[:2]):
            art = r.get("artworkUrl512") or r.get("artworkUrl100")
            if art:
                return art.replace("512x512bb", "1024x1024bb")
    if results:
        art = results[0].get("artworkUrl512") or results[0].get("artworkUrl100")
        if art:
            return art.replace("512x512bb", "1024x1024bb")
    return None


SEARCH_TERMS: dict[str, list[str]] = {
    "tbank": ["T-Bank", "Т-Банк", "Tinkoff"],
    "alfabank": ["Alfa-Bank", "Альфа-Банк"],
    "sberbank": ["Sberbank", "СберБанк"],
    "vtb": ["VTB", "ВТБ Онлайн"],
    "vk": ["VK", "ВКонтакте"],
    "vk-music": ["VK Музыка", "VK Music"],
    "vk-video": ["VK Видео", "VK Video"],
    "youtube": ["YouTube"],
    "yandex-music": ["Яндекс Музыка", "Yandex Music"],
    "ok": ["Одноклассники", "OK.ru"],
    "max": ["MAX мессенджер", "MAX"],
    "rave": ["Rave Watch Party", "Rave"],
    "minecraft": ["Minecraft"],
    "nulls-brawl": ["Nulls Brawl", "Brawl Stars"],
}


def to_webp(raw: bytes, path: Path) -> None:
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = img.size
    if abs(w - h) > 2:
        side = max(w, h)
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
        img = canvas
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    img.save(path, "WEBP", quality=94)


def try_save(app_id: str, raw: bytes, how: str) -> bool:
    path = OUT / f"{app_id}.webp"
    try:
        to_webp(raw, path)
        print(f"  OK via {how} ({path.stat().st_size} bytes)")
        return True
    except Exception as e:
        print(f"  decode fail ({e})")
        return False


def main() -> None:
    for app_id in SOURCES:
        print(f"[{app_id}]")
        # 1) App Store IDs
        for store_id in ITUNES_IDS.get(app_id, []):
            try:
                art = itunes_artwork(store_id)
                if art:
                    if try_save(app_id, fetch(art), f"itunes:{store_id}"):
                        break
            except Exception as e:
                print(f"  itunes id fail: {e}")
        else:
            # 2) Search
            got = False
            for term in SEARCH_TERMS.get(app_id, []):
                for country in ("ru", "us"):
                    try:
                        art = itunes_search(term, country)
                        if art:
                            if try_save(app_id, fetch(art), f"search:{term}:{country}"):
                                got = True
                                break
                    except Exception as e:
                        print(f"  search fail {term}/{country}: {e}")
                if got:
                    break
            if got:
                continue

            # 3) Direct URLs
            for url in SOURCES.get(app_id, []):
                try:
                    if try_save(app_id, fetch(url), url[:60]):
                        break
                except Exception as e:
                    print(f"  url fail: {e}")
            else:
                print("  SKIPPED — no source worked")
        time.sleep(0.3)

    print("\nResult:")
    for p in sorted(OUT.glob("*.webp")):
        print(f"  {p.name:22} {p.stat().st_size:6}")


if __name__ == "__main__":
    main()
