"""Shrink cyan number markers on all 12 instruction images."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

SRC_DIR = Path(r"c:\Users\9rik\Desktop\Фотки для инструкции")
OUT_DIR = Path(r"c:\Users\9rik\Desktop\инсрукция miniapp\public\images")

SCALE = 0.76
TARGET = np.array([0x7D, 0xCB, 0xE8], dtype=np.int16)
TOL = 34

OUT_NAMES = {
    1: "step-1-bot.webp",
    2: "step-2-certificate.webp",
    3: "step-3-esign.webp",
    4: "step-4-developer-mode.webp",
    5: "step-5-files.webp",
    6: "step-6-import.webp",
    7: "step-7-certificate-import.webp",
    8: "step-8-ipa-import.webp",
    9: "step-9-library.webp",
    10: "step-10-apps.webp",
    11: "step-11-sign.webp",
    12: "step-12-install.webp",
}


def find_markers(arr: np.ndarray) -> list[tuple[int, int, int, int]]:
    diff = np.abs(arr.astype(np.int16) - TARGET)
    mask = diff.max(axis=2) < TOL
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    boxes: list[tuple[int, int, int, int]] = []

    for y in range(h):
        ys = mask[y]
        if not ys.any():
            continue
        for x in np.flatnonzero(ys):
            if visited[y, x]:
                continue
            q = deque([(int(x), int(y))])
            visited[y, x] = True
            minx = maxx = int(x)
            miny = maxy = int(y)
            cnt = 0
            while q:
                cx, cy = q.popleft()
                cnt += 1
                for nx, ny in (
                    (cx + 1, cy),
                    (cx - 1, cy),
                    (cx, cy + 1),
                    (cx, cy - 1),
                ):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        q.append((nx, ny))
                        minx = min(minx, nx)
                        maxx = max(maxx, nx)
                        miny = min(miny, ny)
                        maxy = max(maxy, ny)

            bw = maxx - minx + 1
            bh = maxy - miny + 1
            if not (38 <= bw <= 110 and 38 <= bh <= 110):
                continue
            if abs(bw - bh) > 14:
                continue
            if cnt / max(bw * bh, 1) < 0.45:
                continue

            patch = arr[miny : maxy + 1, minx : maxx + 1]
            dark = (patch[..., 0] < 60) & (patch[..., 1] < 70) & (patch[..., 2] < 90)
            if dark.sum() < 40:
                continue

            boxes.append((minx, miny, maxx, maxy))

    return boxes


def erase_mask(arr: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    """Generous mask covering marker + AA halo for clean inpaint."""
    x0, y0, x1, y1 = box
    h, w = arr.shape[:2]
    full = np.zeros((h, w), dtype=np.uint8)

    # Expand bbox a bit to catch soft edges / shadow
    pad = 4
    ex0, ey0 = max(0, x0 - pad), max(0, y0 - pad)
    ex1, ey1 = min(w - 1, x1 + pad), min(h - 1, y1 + pad)
    patch = arr[ey0 : ey1 + 1, ex0 : ex1 + 1]

    cyan = np.abs(patch.astype(np.int16) - TARGET).max(axis=2) < (TOL + 18)
    dark = (patch[..., 0] < 80) & (patch[..., 1] < 90) & (patch[..., 2] < 110)
    # Also grab near-white-cyan mix (AA fringe)
    near = (
        (patch[..., 0] > 140)
        & (patch[..., 1] > 180)
        & (patch[..., 2] > 200)
        & (patch[..., 1] > patch[..., 0] + 10)
    )
    local = (cyan | dark | near).astype(np.uint8) * 255
    local = cv2.dilate(local, np.ones((5, 5), np.uint8), iterations=2)
    # Keep erase limited to rounded area around the square
    local = cv2.morphologyEx(local, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

    full[ey0 : ey1 + 1, ex0 : ex1 + 1] = local
    return full


def shrink_markers(im: Image.Image, boxes: list[tuple[int, int, int, int]]) -> Image.Image:
    rgb = np.array(im.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    erase = np.zeros(rgb.shape[:2], dtype=np.uint8)
    crops: list[tuple[tuple[int, int, int, int], Image.Image]] = []
    for box in boxes:
        x0, y0, x1, y1 = box
        crops.append((box, im.crop((x0, y0, x1 + 1, y1 + 1)).convert("RGBA")))
        erase = cv2.bitwise_or(erase, erase_mask(rgb, box))

    if erase.any():
        bgr = cv2.inpaint(bgr, erase, 6, cv2.INPAINT_NS)

    base = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")

    for box, marker in crops:
        x0, y0, x1, y1 = box
        bw = x1 - x0 + 1
        bh = y1 - y0 + 1
        nw = max(24, int(round(bw * SCALE)))
        nh = max(24, int(round(bh * SCALE)))

        small = marker.resize((nw, nh), Image.Resampling.LANCZOS)

        # Clean rounded mask — no rectangular ghost
        mask = Image.new("L", (nw, nh), 0)
        radius = max(5, int(round(min(nw, nh) * 0.22)))
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw - 1, nh - 1], radius=radius, fill=255)
        # Feather 1px
        mask_np = np.array(mask)
        mask_np = cv2.GaussianBlur(mask_np, (3, 3), 0)
        small.putalpha(Image.fromarray(mask_np))

        cx = x0 + bw // 2
        cy = y0 + bh // 2
        px = cx - nw // 2
        py = cy - nh // 2
        base.alpha_composite(small, (px, py))

    return base.convert("RGB")


def process_one(idx: int, src_name: str) -> None:
    src = SRC_DIR / src_name
    im = Image.open(src).convert("RGB")
    boxes = find_markers(np.array(im))
    print(f"[{idx:02d}] {src_name}: found {len(boxes)} markers {boxes}")
    result = shrink_markers(im, boxes)
    out = OUT_DIR / OUT_NAMES[idx]
    result.save(out, "WEBP", quality=90)
    print(f"     -> {out.name} ({out.stat().st_size // 1024} KB)")


def main() -> None:
    files = {
        1: "step-01.png",
        2: "step-02.png",
        3: "step-03.png",
        4: "step-04.png",
        5: "step-05.png",
        6: "step-06.png",
        7: "step-07.png",
        8: "step-08.png",
        9: "step-09.png",
        10: "step-10.png",
        11: "step-11.png",
        12: "step-12.jpg",
    }
    for i, name in files.items():
        process_one(i, name)
    print("done")


if __name__ == "__main__":
    main()
