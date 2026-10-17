# -*- coding: utf-8 -*-
"""摸合订 PDF 结构：逐页统计文本量/图片数/页面尺寸，输出判界参考。

用法：
    python inspect_pdf.py <pdf路径> [--dpi 100] [--out 渲染目录]

有文本层（字符数>200）的页直读识别；无文本层的扫描页用 --out 渲染 PNG 后目视判界。
"""
import argparse
import os
import re
import sys

import fitz  # PyMuPDF


def inspect(path):
    doc = fitz.open(path)
    print(f"===== {os.path.basename(path)} | 共 {len(doc)} 页 | {os.path.getsize(path):,} B =====")
    for i, page in enumerate(doc, 1):
        text = re.sub(r"\s+", " ", page.get_text()).strip()
        n_img = len(page.get_images(full=True))
        w, h = page.rect.width, page.rect.height
        orient = "横" if w > h else "竖"
        kind = "电子" if len(text) > 200 else ("扫描" if len(text) <= 5 else "少文本")
        preview = text[:60] if text else "(无文本)"
        print(f"P{i:02d} | {kind} | 文本{len(text):5d}字 | 图{n_img} | {orient} | {preview}")
    doc.close()


def render(path, pages, out_dir, dpi):
    """pages: 1-based 页号列表；out_dir: 渲染输出目录。"""
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(path)
    for p in pages:
        if not (1 <= p <= len(doc)):
            print(f"!! P{p} 超出范围（共 {len(doc)} 页），跳过")
            continue
        pix = doc[p - 1].get_pixmap(dpi=dpi)
        fp = os.path.join(out_dir, f"p{p:02d}.png")
        pix.save(fp)
        print(f"rendered P{p:02d} -> {fp}")
    doc.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="合订 PDF 路径")
    ap.add_argument("--dpi", type=int, default=100)
    ap.add_argument("--render", help="要渲染的页号，逗号分隔，如 4,5,9")
    ap.add_argument("--out", default="_pages", help="渲染输出目录")
    a = ap.parse_args()

    if not os.path.exists(a.pdf):
        sys.exit(f"文件不存在: {a.pdf}")
    inspect(a.pdf)
    if a.render:
        pages = [int(x) for x in re.split(r"[,\s]+", a.render.strip()) if x]
        render(a.pdf, pages, a.out, a.dpi)
