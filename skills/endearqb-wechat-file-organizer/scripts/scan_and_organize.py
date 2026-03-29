#!/usr/bin/env python3
"""
微信文件扫描、分类、复制脚本

用法：
  # Dry-run 预览（不执行）
  python scan_and_organize.py --source <源目录> --dest <目标目录> [--mode month_type] [--since 2026-01] --dry-run

  # 正式执行（需要明确不加 --dry-run）
  python scan_and_organize.py --source <源目录> --dest <目标目录> [--mode month_type] [--since 2026-01]
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ── 文件类型分类规则 ─────────────────────────────────────────────
FILE_TYPE_MAP = {
    "图片":  {"jpg", "jpeg", "png", "gif", "webp", "bmp", "heic", "tiff", "ico", "svg"},
    "视频":  {"mp4", "avi", "mov", "mkv", "wmv", "flv", "m4v", "3gp", "ts", "rmvb"},
    "音频":  {"mp3", "wav", "aac", "m4a", "ogg", "opus", "amr", "flac", "wma"},
    "文档":  {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv", "md", "rtf"},
    "压缩包": {"zip", "rar", "7z", "tar", "gz", "bz2", "xz"},
}


def get_file_type(filepath: Path) -> str:
    ext = filepath.suffix.lower().lstrip(".")
    for type_name, exts in FILE_TYPE_MAP.items():
        if ext in exts:
            return type_name
    return "其他"


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_file_month(filepath: Path) -> str:
    try:
        mtime = filepath.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime("%Y-%m")
    except Exception:
        return "未知日期"


def get_dest_subdir(filepath: Path, mode: str) -> str:
    """根据分类模式生成目标子目录"""
    file_type = get_file_type(filepath)
    month_str = get_file_month(filepath)
    if mode == "month_type":
        return os.path.join(month_str, file_type)
    elif mode == "type_only":
        return file_type
    elif mode == "month_only":
        return month_str
    return os.path.join(month_str, file_type)


def is_junk_file(filepath: Path) -> bool:
    """过滤临时文件、空文件"""
    name = filepath.name.lower()
    return (
        name.startswith(".")
        or name.endswith(".tmp")
        or name.endswith(".temp")
        or filepath.stat().st_size == 0
    )


def scan_files(source_dir: str, since_month: str = None) -> tuple:
    """
    扫描源目录，返回 (有效文件列表, 跳过数)
    since_month: "YYYY-MM" 格式，只返回该月及之后的文件
    """
    source = Path(source_dir)
    files = []
    skipped = 0

    for f in source.rglob("*"):
        if not f.is_file():
            continue
        try:
            if is_junk_file(f):
                skipped += 1
                continue
            if since_month:
                month = get_file_month(f)
                if month != "未知日期" and month < since_month:
                    skipped += 1
                    continue
            files.append(f)
        except (OSError, PermissionError):
            skipped += 1

    return files, skipped


def build_copy_plan(files: list, dest_dir: str, mode: str) -> list:
    """
    为每个文件生成 (src, dest) 计划，自动处理目标路径重名
    """
    dest = Path(dest_dir)
    plan = []
    dest_name_count = defaultdict(int)

    for f in files:
        subdir = get_dest_subdir(f, mode)
        dest_folder = dest / subdir
        dest_file = dest_folder / f.name

        # 若目标已在本次计划中重名，加后缀避免覆盖
        dest_key = str(dest_file).lower()
        if dest_name_count[dest_key] > 0:
            dest_file = dest_folder / f"{f.stem}_{dest_name_count[dest_key]}{f.suffix}"
        dest_name_count[dest_key] += 1

        plan.append((f, dest_file))

    return plan


def print_report(source_dir, dest_dir, mode, since_month, files, plan, dry_run):
    """输出整理报告（dry-run 或 正式执行前）"""
    total_size = sum(f.stat().st_size for f in files if f.exists())
    subdir_count = defaultdict(int)
    for src, dest in plan:
        rel = str(Path(dest).parent.relative_to(dest_dir))
        subdir_count[rel] += 1

    since_label = f"{since_month} 至今" if since_month else "全部"
    tag = "（Dry Run 预览）" if dry_run else "（执行中）"

    print("\n" + "=" * 58)
    print(f"📁 微信文件整理{tag}")
    print("=" * 58)
    print(f"源目录：{source_dir}")
    print(f"目标目录：{dest_dir}")
    print(f"分类模式：{mode}    时间范围：{since_label}")
    print()
    print(f"📊 文件统计：")
    print(f"  待整理文件：{len(files):,} 个（共 {format_size(total_size)}）")
    print()
    print(f"📂 目标目录结构：")
    for subdir, count in sorted(subdir_count.items()):
        print(f"  {dest_dir}\\{subdir}\\   → {count:,} 个文件")
    print("=" * 58)
    if dry_run:
        print("\n⚠️  以上为预览，文件尚未复制。")
        print("✅ 确认执行后，将把文件【复制】到目标目录（源文件不删除）。")


def execute_copy(plan: list) -> tuple:
    """执行文件复制，返回 (success, failed, log_lines)"""
    success = 0
    failed = 0
    log_lines = []

    for i, (src, dest) in enumerate(plan):
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))
            success += 1
            log_lines.append(f"[OK] {src} -> {dest}")
        except Exception as e:
            failed += 1
            log_lines.append(f"[FAIL] {src} -> {dest} | {e}")

        if (i + 1) % 100 == 0:
            print(f"  进度：{i+1}/{len(plan)} 个文件...")

    return success, failed, log_lines


def save_log(log_lines: list):
    log_path = Path(__file__).parent.parent / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n整理时间：{timestamp}\n{'='*50}\n")
        for line in log_lines:
            f.write(line + "\n")
    return str(log_path)


def update_config_last_run(source_dir, dest_dir, mode):
    config_path = Path(__file__).parent.parent / "config.json"
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass
    config.update({
        "source_dir": source_dir,
        "dest_dir": dest_dir,
        "mode": mode,
        "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="微信文件分类整理工具")
    parser.add_argument("--source", required=True, help="微信文件源目录")
    parser.add_argument("--dest",   required=True, help="整理后保存目录")
    parser.add_argument("--mode", default="month_type",
                        choices=["month_type", "type_only", "month_only"],
                        help="分类模式")
    parser.add_argument("--since", default=None,
                        help="只处理该月份及之后的文件，格式 YYYY-MM，如 2026-01")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅预览，不执行任何操作")
    args = parser.parse_args()

    if not Path(args.source).exists():
        print(f"❌ 源目录不存在：{args.source}")
        sys.exit(1)

    print(f"🔍 正在扫描：{args.source} ...")
    files, skipped = scan_files(args.source, args.since)
    print(f"   发现 {len(files):,} 个有效文件（跳过 {skipped:,} 个临时/范围外文件）")

    print("📋 正在生成整理计划...")
    plan = build_copy_plan(files, args.dest, args.mode)

    print_report(args.source, args.dest, args.mode, args.since, files, plan, args.dry_run)

    if args.dry_run:
        print("\n[Dry-run 模式，未执行任何文件操作]")
        return

    # 正式执行
    print(f"\n🚀 开始整理，共 {len(plan):,} 个文件...")
    success, failed, log_lines = execute_copy(plan)
    log_path = save_log(log_lines)
    update_config_last_run(args.source, args.dest, args.mode)

    print(f"\n✅ 整理完成！")
    print(f"   成功复制：{success:,} 个文件")
    if failed:
        print(f"   失败：{failed:,} 个文件")
    print(f"   日志：{log_path}")


if __name__ == "__main__":
    main()
