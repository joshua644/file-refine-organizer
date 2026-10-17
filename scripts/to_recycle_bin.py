# -*- coding: utf-8 -*-
"""将指定文件/目录移入 Windows 回收站（SHFileOperationW + FOF_ALLOWUNDO），不彻底删除。

用法：
    python to_recycle_bin.py <路径1> [路径2 ...]     # 绝对路径，可多个
"""
import argparse
import ctypes
import os
from ctypes import wintypes

FOF_ALLOWUNDO = 0x0040
FOF_NOCONFIRMATION = 0x0010
FOF_SILENT = 0x0004
FO_DELETE = 0x0003


class SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("wFunc", wintypes.UINT),
        ("pFrom", wintypes.LPCWSTR),
        ("pTo", wintypes.LPCWSTR),
        ("fFlags", wintypes.USHORT),
        ("fAnyOperationsAborted", wintypes.BOOL),
        ("hNameMappings", wintypes.LPVOID),
        ("lpszProgressTitle", wintypes.LPCWSTR),
    ]


def to_recycle_bin(paths):
    """paths: list[str]，每个必须是绝对路径；目录需以双 NUL 结尾由函数统一处理。"""
    buf = "\0".join(paths) + "\0\0"
    op = SHFILEOPSTRUCTW()
    op.wFunc = FO_DELETE
    op.pFrom = buf
    op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT
    res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
    return res, op.fAnyOperationsAborted


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="把指定文件/目录移入 Windows 回收站（不彻底删除，可恢复）")
    ap.add_argument("paths", nargs="+", help="要移入回收站的绝对路径（可多个）")
    a = ap.parse_args()

    res, aborted = to_recycle_bin(a.paths)
    print(f"SHFileOperation 返回码: {res} (0=成功)")
    print(f"操作被中止: {bool(aborted)}")

    for t in a.paths:
        print(("仍存在(未删成功): " if os.path.exists(t) else "已移入回收站: ") + t)
