# -*- coding: utf-8 -*-
"""按页区间拆分合订 PDF，并做双项校验（页数合计 == 原总页数；逐件首页文本预览）。

用法：
    1. 改下方 JOBS：每个任务 = (源PDF路径, 输出文件夹, [(输出文件名, 起始页, 结束页), ...])，页码 1-based 含端点
    2. python split_pdf.py

约定（file-refine-organizer）：
    - 输出文件夹名 = 日期_采购报销_项目简称_事项_比例_金额_合同号或供应商
    - 00_ 主单（OA 单号+金额）；附件N_ 按装订顺序；无主单从附件1 起编
    - 合同包（组成合同的文件列为一套的）保持一个整件不拆
    - 只留拆分件：原合订 PDF 拆完移暂存区（to_recycle_bin.py 清空）
"""
import os
import re
import sys

import fitz  # PyMuPDF

# ============ 页区间表（每次拆分改这里） ============
# (源PDF绝对路径, 输出文件夹绝对路径, [(输出文件名, 起页, 止页), ...])
JOBS = [
    # 示例（把尖括号占位符换成实际值）：
    # (
    #     r"D:\...\20260509_采购报销_XX项目_支付01_6600_HT0001.pdf",
    #     r"D:\...\01-发票与请款资料\20260509_采购报销_XX项目_支付01_6600_HT0001",
    #     [
    #         ("00_采购报销单_<OA单号>_6600.pdf", 1, 2),
    #         ("附件1_电子发票_普通发票_<发票号>_6600.pdf", 3, 3),
    #         ("附件6_合同_HT0001_33000.pdf", 9, 31),
    #     ],
    # ),
]


def split_one(src, folder, ranges):
    os.makedirs(folder, exist_ok=True)
    doc = fitz.open(src)
    total_src = len(doc)
    total_out = 0
    print(f"----- {os.path.basename(folder)} -----")
    for name, p1, p2 in ranges:
        if not (1 <= p1 <= p2 <= total_src):
            print(f"!! {name}: 页区间 P{p1}-{p2} 非法（共 {total_src} 页）")
            doc.close()
            return False
        out_path = os.path.join(folder, name)
        nd = fitz.open()
        nd.insert_pdf(doc, from_page=p1 - 1, to_page=p2 - 1, garbage=3, deflate=True)
        nd.save(out_path)
        first = re.sub(r"\s+", " ", nd[0].get_text()).strip()[:45]
        print(f"{name} | P{p1:02d}-{p2:02d} {p2 - p1 + 1}页 | 首页: {first}")
        total_out += len(nd)
        nd.close()
    doc.close()
    ok = total_out == total_src
    print(f"合计 {total_out} 页 / 原件 {total_src} 页 -> {'PASS' if ok else '!!FAIL!!'}")
    return ok


if __name__ == "__main__":
    if not JOBS:
        sys.exit("JOBS 为空：先在脚本头部填入页区间表再运行")
    all_ok = True
    for src, folder, ranges in JOBS:
        if not os.path.exists(src):
            print(f"!! 源文件不存在: {src}")
            all_ok = False
            continue
        all_ok = split_one(src, folder, ranges) and all_ok
    print("\n全部校验通过" if all_ok else "\n存在失败项，检查后重跑")
    sys.exit(0 if all_ok else 1)
