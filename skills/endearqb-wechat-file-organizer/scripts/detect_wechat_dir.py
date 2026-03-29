#!/usr/bin/env python3
"""
检测 Windows 微信文件存储目录
覆盖场景：
  - 默认安装路径 (Documents/WeChat Files)
  - 电脑管家迁移路径 (xwechat_files)
  - 自定义安装路径
"""

import os
import json
from pathlib import Path

# 配置文件放在 skill 根目录（scripts/ 的上一级）
SKILL_ROOT  = Path(__file__).parent.parent
CONFIG_PATH = SKILL_ROOT / "config.json"
LOG_PATH    = SKILL_ROOT / "organizer_log.txt"


def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def save_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_all_drives():
    """获取 Windows 所有可用盘符"""
    drives = []
    for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        p = Path(f"{letter}:/")
        if p.exists():
            drives.append(p)
    return drives


def count_files_fast(directory: str, max_count: int = 5000) -> tuple:
    """快速统计文件数和总大小（超过 max_count 停止，返回 truncated=True）"""
    path = Path(directory)
    total_files = 0
    total_size = 0
    try:
        for f in path.rglob("*"):
            if f.is_file():
                total_files += 1
                try:
                    total_size += f.stat().st_size
                except (OSError, PermissionError):
                    pass
                if total_files >= max_count:
                    return total_files, total_size, True
    except (PermissionError, OSError):
        pass
    return total_files, total_size, False


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def find_wechat_dirs() -> list:
    """
    多策略检测微信文件目录，返回候选路径列表
    每项: {path, label, file_count, total_size, truncated}
    """
    found = {}  # 用 path 小写做 key 去重

    def add_candidate(path: Path, label: str):
        key = str(path).lower()
        if key in found or not path.exists():
            return
        count, size, truncated = count_files_fast(str(path))
        if count == 0:
            return
        found[key] = {
            "path": str(path),
            "label": label,
            "file_count": count,
            "total_size": size,
            "truncated": truncated,
        }

    # ── 策略1：标准默认路径 ──────────────────────────────────
    home = Path.home()
    user_profile = os.environ.get("USERPROFILE", "")
    base_dirs = [
        home / "Documents" / "WeChat Files",
        home / "文档" / "WeChat Files",
        home / "我的文档" / "WeChat Files",
    ]
    if user_profile:
        up = Path(user_profile)
        base_dirs += [up / "Documents" / "WeChat Files", up / "文档" / "WeChat Files"]

    for base in base_dirs:
        if not base.exists():
            continue
        # 优先找账号子目录下的文件存储位置
        matched_sub = False
        for pattern in ["*/msg/file", "*/msg/File", "*/FileStorage"]:
            for d in base.glob(pattern):
                if d.is_dir():
                    add_candidate(d, f"微信默认路径（{d.parts[-3]}）")
                    matched_sub = True
        if not matched_sub:
            add_candidate(base, "微信默认路径")

    # ── 策略2：电脑管家 / 迁移工具路径 ──────────────────────
    # 典型：D:\电脑管家迁移文件\xwechat_files\wxid_xxx\msg\file
    try:
        for drive in get_all_drives():
            # 只扫描一级子目录，避免全盘递归太慢
            for top in drive.iterdir():
                if not top.is_dir():
                    continue
                xwechat = top / "xwechat_files"
                if xwechat.is_dir():
                    for pattern in ["*/msg/file", "*/msg/File", "*/FileStorage"]:
                        for d in xwechat.glob(pattern):
                            if d.is_dir():
                                add_candidate(d, f"电脑管家迁移（{d.parts[-3]}）")
    except (PermissionError, OSError):
        pass

    # ── 策略3：其他盘符下的非标准 WeChat Files ───────────────
    try:
        for drive in get_all_drives():
            for top in drive.iterdir():
                if not top.is_dir():
                    continue
                wf = top / "WeChat Files"
                if wf.is_dir():
                    for pattern in ["*/msg/file", "*/FileStorage"]:
                        for d in wf.glob(pattern):
                            if d.is_dir():
                                add_candidate(d, f"自定义路径（{top.name}/WeChat Files/{d.parts[-3]}）")
    except (PermissionError, OSError):
        pass

    return list(found.values())


def main():
    print("🔍 正在检测微信文件存储目录...\n")

    # 先检查已保存配置
    config = load_config()
    if config and config.get("source_dir"):
        source = Path(config["source_dir"])
        if source.exists():
            count, size, _ = count_files_fast(str(source))
            print("✅ 发现已保存的配置：")
            print(f"   源目录：{source}")
            print(f"   目标目录：{config.get('dest_dir', '未设置')}")
            print(f"   文件数：{count:,} 个（{format_size(size)}）")
            if config.get("last_run"):
                print(f"   上次整理：{config['last_run']}")
            print("\n输入 'reset' 可重新配置，否则将沿用此配置。")
            return {"status": "found_config", "config": config}
        else:
            print(f"⚠️  已保存配置中的源目录不存在：{source}")
            print("将重新检测...\n")

    # 自动检测
    candidates = find_wechat_dirs()

    if not candidates:
        print("❌ 未自动检测到微信文件目录。")
        print("\n请手动输入微信文件存储路径，常见位置：")
        print(r"  · C:\Users\{用户名}\Documents\WeChat Files\wxid_xxx\msg\file")
        print(r"  · D:\电脑管家迁移文件\xwechat_files\wxid_xxx\msg\file")
        return {"status": "not_found", "candidates": []}

    print(f"✅ 检测到 {len(candidates)} 个候选目录：\n")
    for i, c in enumerate(candidates, 1):
        size_str = format_size(c["total_size"])
        count_str = f"{c['file_count']:,}+" if c["truncated"] else f"{c['file_count']:,}"
        print(f"  [{i}] {c['path']}")
        print(f"      {c['label']}  ·  {count_str} 个文件  ·  {size_str}\n")

    status = "found_single" if len(candidates) == 1 else "found_multiple"
    return {
        "status": status,
        "candidates": candidates,
        "recommended": candidates[0]["path"],
    }


if __name__ == "__main__":
    import json as _json
    result = main()
    print("\n---RESULT---")
    print(_json.dumps(result, ensure_ascii=False, indent=2))
