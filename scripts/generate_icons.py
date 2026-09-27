from pathlib import Path

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

for sid, (bg, fg, letter) in icons.items():
    size = 36 if len(letter) > 1 else 48
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#g)"/>
  <text x="64" y="74" text-anchor="middle" font-family="-apple-system,Segoe UI,sans-serif" font-size="{size}" font-weight="700" fill="{fg}">{letter}</text>
</svg>
"""
    (out / f"{sid}.svg").write_text(svg, encoding="utf-8")
    print(sid)

print("icons done")
