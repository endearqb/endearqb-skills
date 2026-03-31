#!/usr/bin/env python3
"""
微信重复文件检测 + 移入回收站

去重逻辑：
  A. 括号序号重复：文件(1).ext、文件(2).ext → 与 文件.ext 归为一组（大小必须相同）
  B. 完全相同重复：文件名完全相同 + 大小完全相同

保留策略：每组中保留修改时间最新的文件，其余移入回收站。
安全原则：仅操作回收站，不永久删除。

用法：
  python dedup_recycle.py --source <源目录> --dry-run   # 预览
  python dedup_recycle.py --source <源目录>             # 执行
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ── 工具函数 ─────────────────────────────────────────────────────

def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# 匹配微信括号序号：文件名 (N).ext 或 文件名(N).ext（N 为数字）
BRACKET_PATTERN = re.compile(r"^(.+?)\s*\((\d+)\)$")


def get_base_name(stem: str) -> str:
    """
    提取基础文件名（去掉括号序号）
    'report (2)'  -> 'report'
    'report_v2'   -> 'report_v2'  （不匹配，原样返回）
    """
    m = BRACKET_PATTERN.match(stem)
    return m.group(1).rstrip() if m else stem


def get_mtime(f: Path) -> float:
    try:
        return f.stat().st_mtime
    except (OSError, PermissionError):
        return 0.0


def get_size(f: Path) -> int:
    try:
        return f.stat().st_size
    except (OSError, PermissionError):
        return -1


# ── 核心去重逻辑 ──────────────────────────────────────────────────

def find_duplicates_by_size(source_dir: str) -> list:
    """
    基于文件大小查找重复（用于哈希命名的视频文件）
    返回重复文件组列表
    """
    source = Path(source_dir)
    size_map = defaultdict(list)

    # 按大小分组
    for f in source.rglob("*"):
        if not f.is_file():
            continue
        size = get_size(f)
        if size <= 0:
            continue
        size_map[size].append((f, get_mtime(f)))

    # 筛选出有重复（大小相同）的组
    result = []
    for size, files in size_map.items():
        if len(files) < 2:
            continue

        # 按修改时间降序，保留最新的
        files.sort(key=lambda x: x[1], reverse=True)
        keep_file = files[0][0]
        remove_files = [f[0] for f in files[1:]]

        result.append({
            "keep": keep_file,
            "remove": remove_files,
            "reason": "大小相同重复",
            "size_each": size,
        })

    return result


def find_duplicate_groups(source_dir: str) -> list:
    """
    扫描目录，返回重复文件组列表
    每组: {"keep": Path, "remove": [Path, ...], "reason": str}
    """
    source = Path(source_dir)

    # 收集所有文件，按 (基础名小写, 扩展名小写, 大小) 分组
    # key -> [(Path, mtime, is_numbered)]
    groups: dict = defaultdict(list)

    for f in source.rglob("*"):
        if not f.is_file():
            continue
        size = get_size(f)
        if size <= 0:
            continue

        stem = f.stem
        ext = f.suffix.lower()
        base = get_base_name(stem)
        is_numbered = (base != stem)

        # 分组 key：基础名（小写）+ 扩展名 + 大小
        # 大小不同 → 不视为重复（可能是真不同版本）
        key = (base.lower(), ext, size)
        groups[key].append((f, get_mtime(f), is_numbered))

    # 筛选出有重复的组
    result = []
    for key, members in groups.items():
        if len(members) < 2:
            continue

        base_name, ext, size = key

        # 按修改时间降序排列，保留最新的
        members.sort(key=lambda x: x[1], reverse=True)
        keep_file = members[0][0]
        remove_files = [m[0] for m in members[1:]]

        # 判断去重原因
        has_numbered = any(m[2] for m in members)
        reason = "括号序号重复" if has_numbered else "完全相同重复"

        result.append({
            "keep": keep_file,
            "remove": remove_files,
            "reason": reason,
            "size_each": size,
        })

    return result


# ── 回收站操作 ────────────────────────────────────────────────────

def move_to_recycle_bin_windows(file_path: Path) -> bool:
    """
    将文件移入 Windows 回收站
    优先使用 send2trash（需安装），回退到 PowerShell Shell API
    """
    # 方法1：send2trash（最可靠，推荐安装）
    try:
        import send2trash
        send2trash.send2trash(str(file_path))
        return True
    except ImportError:
        pass
    except Exception:
        pass

    # 方法2：ctypes SHFileOperation（内置，无需安装）
    try:
        import ctypes
        # SHFILEOPSTRUCT 简化版
        class SHFILEOPSTRUCT(ctypes.Structure):
            _fields_ = [
                ("hwnd",                ctypes.c_void_p),
                ("wFunc",               ctypes.c_uint),
                ("pFrom",               ctypes.c_wchar_p),
                ("pTo",                 ctypes.c_wchar_p),
                ("fFlags",              ctypes.c_ushort),
                ("fAnyOperationsAborted", ctypes.c_bool),
                ("hNameMappings",       ctypes.c_void_p),
                ("lpszProgressTitle",   ctypes.c_wchar_p),
            ]

        FO_DELETE = 0x0003
        FOF_ALLOWUNDO      = 0x0040  # 放入回收站（而非永久删除）
        FOF_NOCONFIRMATION = 0x0010
        FOF_NOERRORUI      = 0x0400
        FOF_SILENT         = 0x0004

        op = SHFILEOPSTRUCT()
        op.hwnd = None
        op.wFunc = FO_DELETE
        op.pFrom = str(file_path) + "\0"  # 必须以双 \0 结尾（c_wchar_p 会自动加一个）
        op.pTo = None
        op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_SILENT
        op.fAnyOperationsAborted = False

        result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
        return result == 0
    except Exception:
        pass

    # 方法3：PowerShell 回退（最后手段）
    try:
        ps_script = (
            "Add-Type -AssemblyName Microsoft.VisualBasic; "
            f"[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("
            f"'{str(file_path)}', 'OnlyErrorDialogs', 'SendToRecycleBin')"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, timeout=10
        )
        return result.returncode == 0
    except Exception:
        pass

    return False


# ── 主流程 ────────────────────────────────────────────────────────

def print_dry_run_report(source_dir: str, groups: list):
    total_remove = sum(len(g["remove"]) for g in groups)
    total_size_saved = sum(g["size_each"] * len(g["remove"]) for g in groups)
    bracket_groups = [g for g in groups if g["reason"] == "括号序号重复"]
    exact_groups   = [g for g in groups if g["reason"] == "完全相同重复"]
    size_groups    = [g for g in groups if g["reason"] == "大小相同重复"]

    print("\n" + "=" * 58)
    print("🗑  微信重复文件检测报告（Dry Run 预览）")
    print("=" * 58)
    print(f"扫描目录：{source_dir}")
    print()
    print(f"📊 统计：")
    print(f"  发现重复组：   {len(groups):,} 组")
    if bracket_groups or exact_groups:
        print(f"    括号序号重复：{len(bracket_groups):,} 组（如 文件(2).pdf）")
        print(f"    完全相同重复：{len(exact_groups):,} 组")
    if size_groups:
        print(f"    大小相同重复：{len(size_groups):,} 组（哈希命名文件）")
    print(f"  将移入回收站：{total_remove:,} 个文件（节省 {format_size(total_size_saved)}）")
    print()

    print(f"🗂  重复详情（前20组）：")
    print(f"  {'保留文件':<40} {'移除文件（进回收站）'}")
    print(f"  {'-'*40} {'-'*30}")
    for g in groups[:20]:
        keep_name = g["keep"].name
        for rm in g["remove"]:
            keep_show = keep_name[:38] + ".." if len(keep_name) > 40 else keep_name
            rm_show = rm.name[:28] + ".." if len(rm.name) > 30 else rm.name
            print(f"  ✅ {keep_show:<40} ❌ {rm_show}  ({format_size(g['size_each'])})")
    if len(groups) > 20:
        print(f"  ... 共 {len(groups)} 组，仅显示前20组")

    print()
    print("=" * 58)
    print("⚠️  以上为预览，文件尚未移动。")
    print("✅ 确认执行后，重复文件将移入【回收站】（可恢复）。")


def main():
    parser = argparse.ArgumentParser(description="微信重复文件检测 & 回收站清理")
    parser.add_argument("--source", required=True, help="微信文件源目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行任何操作")
    parser.add_argument("--by-size", action="store_true", help="基于文件大小去重（用于哈希命名文件，如视频）")
    args = parser.parse_args()

    if not Path(args.source).exists():
        print(f"❌ 源目录不存在：{args.source}")
        sys.exit(1)

    if args.by_size:
        print(f"🔍 正在基于【文件大小】扫描重复：{args.source} ...")
        groups = find_duplicates_by_size(args.source)
    else:
        print(f"🔍 正在扫描重复文件：{args.source} ...")
        groups = find_duplicate_groups(args.source)

    if not groups:
        print("✅ 未发现重复文件，目录很整洁！")
        return

    print_dry_run_report(args.source, groups)

    if args.dry_run:
        print("\n[Dry-run 模式，未执行任何操作]")
        return

    # 正式执行
    total_remove = sum(len(g["remove"]) for g in groups)
    print(f"\n🚀 开始将 {total_remove} 个重复文件移入回收站...")

    success = 0
    failed = 0
    failed_files = []

    for g in groups:
        for rm in g["remove"]:
            if not rm.exists():
                continue
            ok = move_to_recycle_bin_windows(rm)
            if ok:
                success += 1
            else:
                failed += 1
                failed_files.append(str(rm))

    print(f"\n✅ 完成！")
    print(f"   成功移入回收站：{success:,} 个文件")
    if failed:
        print(f"   失败：{failed:,} 个文件")
        for f in failed_files[:5]:
            print(f"     - {f}")
        if len(failed_files) > 5:
            print(f"     ... 共 {len(failed_files)} 个")

    # 保存操作日志
    log_path = Path(__file__).parent.parent / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as lf:
        lf.write(f"\n{'='*50}\n去重时间：{timestamp}\n{'='*50}\n")
        for g in groups:
            for rm in g["remove"]:
                status = "OK" if rm not in failed_files else "FAIL"
                lf.write(f"[{status}] 回收站 <- {rm}  (保留: {g['keep'].name})\n")
    print(f"   日志：{log_path}")

    print("\n💡 提示：所有文件在回收站中可随时还原。")


if __name__ == "__main__":
    main()
