#!/usr/bin/env python3
"""render_preview.py — pptx → pdf → 逐页 png → contact sheet。

用法:
    python scripts/render_preview.py out/deck.pptx
    python scripts/render_preview.py out/deck.pptx --outdir out/deck_preview --dpi 80 --cols 4

产物（默认 <pptx 同目录>/<名>_preview/）:
    deck.pdf
    slide-01.png, slide-02.png, ...
    contact_sheet.png        全部页面缩略 + 页码，先看这张

退出码:
    0 成功
    3 缺少 soffice 或 pdftoppm
    4 转换失败

替代方案（缺依赖时）:
    - macOS:  brew install --cask libreoffice && brew install poppler
    - Ubuntu: sudo apt install libreoffice-impress poppler-utils
    - 都装不了：用 PowerPoint / Keynote 导出 PDF，再运行
      python scripts/render_preview.py out/deck.pdf   （直接传 pdf 也可以）
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    print("缺少依赖: pip install pillow", file=sys.stderr)
    sys.exit(2)


def find_soffice() -> str | None:
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    for p in ("/Applications/LibreOffice.app/Contents/MacOS/soffice",
              "C:\\Program Files\\LibreOffice\\program\\soffice.exe"):
        if os.path.exists(p):
            return p
    return None


def to_pdf(pptx: str, outdir: str) -> str:
    soffice = find_soffice()
    if not soffice:
        print("找不到 soffice（LibreOffice）。见脚本头部替代方案。", file=sys.stderr)
        sys.exit(3)
    cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", outdir, pptx]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")
    if r.returncode != 0 or not os.path.isfile(pdf):
        print(f"soffice 转换失败:\n{r.stdout}\n{r.stderr}", file=sys.stderr)
        sys.exit(4)
    return pdf


def to_pngs(pdf: str, outdir: str, dpi: int) -> list[str]:
    if not shutil.which("pdftoppm"):
        print("找不到 pdftoppm（poppler）。见脚本头部替代方案。", file=sys.stderr)
        sys.exit(3)
    for old in glob.glob(os.path.join(outdir, "slide-*.png")):
        os.remove(old)
    prefix = os.path.join(outdir, "slide")
    r = subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, prefix], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print(f"pdftoppm 失败:\n{r.stderr}", file=sys.stderr)
        sys.exit(4)
    files = sorted(glob.glob(prefix + "-*.png"))
    # pdftoppm 命名 slide-1.png / slide-01.png 取决于页数；统一成两位
    renamed = []
    for f in files:
        num = int(os.path.splitext(f)[0].rsplit("-", 1)[1])
        nf = os.path.join(outdir, f"slide-{num:02d}.png")
        if nf != f:
            os.replace(f, nf)
        renamed.append(nf)
    return sorted(renamed)


def contact_sheet(pngs: list[str], out: str, cols: int = 4, thumb_w: int = 480, pad: int = 24) -> str:
    if not pngs:
        raise ValueError("没有页面图片")
    with Image.open(pngs[0]) as im0:
        ratio = im0.size[1] / im0.size[0]
    thumb_h = int(thumb_w * ratio)
    rows = (len(pngs) + cols - 1) // cols
    label_h = 28
    W = cols * thumb_w + (cols + 1) * pad
    H = rows * (thumb_h + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), "#202225")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, p in enumerate(pngs):
        r, c = divmod(i, cols)
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + label_h + pad)
        with Image.open(p) as im:
            im = im.convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
            sheet.paste(im, (x, y))
        draw.rectangle([x, y, x + thumb_w - 1, y + thumb_h - 1], outline="#3A3D44", width=1)
        draw.text((x, y + thumb_h + 6), f"{i + 1:02d}", fill="#E8E8E8", font=font)
    sheet.save(out, "PNG", optimize=True)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help=".pptx 或已导出的 .pdf")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--dpi", type=int, default=80, help="逐页 PNG 分辨率；细看用 150")
    ap.add_argument("--cols", type=int, default=4)
    args = ap.parse_args(argv)

    src = os.path.abspath(args.input)
    if not os.path.isfile(src):
        print(f"文件不存在: {src}", file=sys.stderr)
        return 2
    base = os.path.splitext(os.path.basename(src))[0]
    outdir = os.path.abspath(args.outdir or os.path.join(os.path.dirname(src), f"{base}_preview"))
    os.makedirs(outdir, exist_ok=True)

    pdf = src if src.lower().endswith(".pdf") else to_pdf(src, outdir)
    pngs = to_pngs(pdf, outdir, args.dpi)
    sheet = contact_sheet(pngs, os.path.join(outdir, "contact_sheet.png"), cols=args.cols)

    print(f"→ {pdf}")
    print(f"→ {len(pngs)} 页 PNG: {outdir}/slide-XX.png")
    print(f"→ contact sheet: {sheet}")
    print("\n下一步：打开 contact sheet 逐页看，对照 references/qa-checklist.md；"
          "然后运行 python scripts/inspect_pptx.py。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
