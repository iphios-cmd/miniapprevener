import json
import ssl
import urllib.parse
import urllib.request

ctx = ssl.create_default_context()


def search(term: str, country: str = "ru") -> None:
    qs = urllib.parse.urlencode(
        {"term": term, "country": country, "entity": "software", "limit": 6}
    )
    data = json.loads(
        urllib.request.urlopen(
            "https://itunes.apple.com/search?" + qs, context=ctx, timeout=20
        ).read()
    )
    for r in data.get("results", []):
        name = (r.get("trackName") or "")[:42]
        bid = r.get("bundleId")
        art = (r.get("artworkUrl512") or "")[:70]
        print(f"  {name} | {bid} | {art}")


for t in [
    "Sberbank",
    "СберБанк Онлайн",
    "VTB Online",
    "ВТБ Онлайн",
    "VK Music",
    "VK Музыка",
    "Rave - Watch Party",
    "MAX Messenger",
    "Nulls Brawl",
    "Alfa-Bank",
]:
    print("===", t)
    search(t)
    if t in ("Sberbank", "VTB Online", "Rave - Watch Party"):
        print("--- us ---")
        search(t, "us")
