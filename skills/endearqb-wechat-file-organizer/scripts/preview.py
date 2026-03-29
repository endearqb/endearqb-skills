#!/usr/bin/env python3
"""
微信文件整理 - 统一预览脚本

一次性展示：
  1. 重复文件分析（将移入回收站的）
  2. 整理后的目录结构预览（将复制到目标目录的）

用法：
  python preview.py --source <源目录> --dest <目标目录> [--mode month_type] [--since 2026-01]

不执行任何文件操作，纯预览。
"""

import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# 复用已有模块
sys.path.insert(0, str(Path(__file__).parent))
from dedup_recycle import find_duplicate_groups, format_size as fmt_size
from scan_and_organize import scan_files, build_copy_plan, get_file_type, get_file_month


def print_full_preview(source_dir, dest_dir, mode, since_month):
    source = Path(source_dir)

    print("\n" + "=" * 62)
    print("📋 微信文件整理完整预览")
    print("=" * 62)
    print(f"源目录：{source_dir}")
    print(f"目标目录：{dest_dir}")
    since_label = f"{since_month} 至今" if since_month else "全部"
    print(f"分类模式：{mode}    时间范围：{since_label}")

    # ── Part 1：重复文件分析 ───────────────────────────────────────
    print("\n" + "─" * 62)
    print("🗑  Part 1 · 重复文件（将移入回收站）")
    print("─" * 62)

    groups = find_duplicate_groups(source_dir)

    if not groups:
        print("  ✅ 未发现重复文件")
    else:
        total_remove = sum(len(g["remove"]) for g in groups)
        total_saved  = sum(g["size_each"] * len(g["remove"]) for g in groups)
        bracket_cnt  = sum(1 for g in groups if g["reason"] == "括号序号重复")
        exact_cnt    = sum(1 for g in groups if g["reason"] == "完全相同重复")

        print(f"  发现重复组：{len(groups):,} 组  →  将移入回收站：{total_remove:,} 个文件（节省 {fmt_size(total_saved)}）")
        print(f"    括号序号重复：{bracket_cnt} 组（如 文件(2).pdf）")
        print(f"    完全相同重复：{exact_cnt} 组")
        print()

        # 按月份汇总重复文件
        month_remove_count = defaultdict(int)
        month_remove_size  = defaultdict(int)
        for g in groups:
            for rm in g["remove"]:
                m = get_file_month(rm)
                month_remove_count[m] += 1
                month_remove_size[m]  += g["size_each"]

        print(f"  {'月份':<12} {'重复文件数':>10} {'节省空间':>12}")
        print(f"  {'-'*12} {'-'*10} {'-'*12}")
        for month in sorted(month_remove_count.keys()):
            print(f"  {month:<12} {month_remove_count[month]:>10,} 个  {fmt_size(month_remove_size[month]):>10}")

        print()
        print(f"  示例（前15组）：")
        print(f"  {'保留':<36}  {'移除（→回收站）'}")
        print(f"  {'-'*36}  {'-'*28}")
        for g in groups[:15]:
            keep_show = g["keep"].name
            if len(keep_show) > 35:
                keep_show = keep_show[:33] + ".."
            for rm in g["remove"]:
                rm_show = rm.name
                if len(rm_show) > 28:
                    rm_show = rm_show[:26] + ".."
                print(f"  ✅ {keep_show:<35}  ❌ {rm_show}  ({fmt_size(g['size_each'])})")
        if len(groups) > 15:
            print(f"  ... 共 {len(groups)} 组，仅显示前15组")

    # ── Part 2：整理后目录结构 ─────────────────────────────────────
    print()
    print("─" * 62)
    print("📂 Part 2 · 整理后目录结构（将复制到目标目录）")
    print("─" * 62)

    files, skipped = scan_files(source_dir, since_month)

    if not files:
        print("  ⚠️  没有符合条件的文件可整理")
    else:
        plan = build_copy_plan(files, dest_dir, mode)
        total_size = sum(f.stat().st_size for f in files if f.exists())

        # 按子目录统计
        subdir_stats = defaultdict(lambda: {"count": 0, "size": 0})
        for src, dest in plan:
            rel = str(Path(dest).parent.relative_to(dest_dir))
            subdir_stats[rel]["count"] += 1
            try:
                subdir_stats[rel]["size"] += src.stat().st_size
            except (OSError, PermissionError):
                pass

        # 按月份+类型汇总
        type_total = defaultdict(int)
        for src, _ in plan:
            type_total[get_file_type(src)] += 1

        print(f"  待整理文件：{len(files):,} 个（共 {fmt_size(total_size)}）")
        print(f"  跳过文件：  {skipped:,} 个（临时文件 / 时间范围外）")
        print()

        # 文件类型汇总
        print(f"  文件类型分布：")
        for t, cnt in sorted(type_total.items(), key=lambda x: -x[1]):
            bar = "█" * min(cnt // max(1, len(files) // 20), 20)
            print(f"    {t:<6} {cnt:>5,} 个  {bar}")

        print()
        print(f"  目标目录结构：")
        for subdir, stat in sorted(subdir_stats.items()):
            size_str = fmt_size(stat["size"])
            print(f"    {dest_dir}\\{subdir}\\")
            print(f"      → {stat['count']:,} 个文件  ·  {size_str}")

    # ── 总结 ──────────────────────────────────────────────────────
    print()
    print("=" * 62)
    print("📌 操作建议")
    print("=" * 62)

    steps = []
    if groups:
        total_remove = sum(len(g["remove"]) for g in groups)
        total_saved  = sum(g["size_each"] * len(g["remove"]) for g in groups)
        steps.append(f"步骤 A · 清理重复文件 → 将 {total_remove} 个文件移入回收站（释放 {fmt_size(total_saved)}）")
        steps.append(f"         命令：python dedup_recycle.py --source \"{source_dir}\"")

    if files:
        steps.append(f"步骤 B · 整理文件到目标目录 → 复制 {len(files):,} 个文件")
        since_arg = f' --since {since_month}' if since_month else ''
        steps.append(f"         命令：python scan_and_organize.py --source \"{source_dir}\" --dest \"{dest_dir}\" --mode {mode}{since_arg}")

    if steps:
        for s in steps:
            print(f"  {s}")
    else:
        print("  ✅ 无需任何操作")

    print()
    print("⚠️  以上为完整预览，确认后请告知执行哪些步骤。")
    print("=" * 62)


def main():
    parser = argparse.ArgumentParser(description="微信文件整理 - 统一预览")
    parser.add_argument("--source", required=True, help="微信文件源目录")
    parser.add_argument("--dest",   required=True, help="整理后保存目录")
    parser.add_argument("--mode", default="month_type",
                        choices=["month_type", "type_only", "month_only"])
    parser.add_argument("--since", default=None, help="只预览该月份及之后，格式 YYYY-MM")
    args = parser.parse_args()

    if not Path(args.source).exists():
        print(f"❌ 源目录不存在：{args.source}")
        sys.exit(1)

    print(f"🔍 正在分析：{args.source} ...")
    print(f"   （首次分析较慢，文件较多时请耐心等待）")

    print_full_preview(args.source, args.dest, args.mode, args.since)


if __name__ == "__main__":
    main()
