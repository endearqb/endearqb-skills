---
name: wechat-file-organizer
description: 整理 Windows 微信聊天文件存储目录的技能。当用户说"整理微信文件"、"清理微信缓存"、"整理微信图片/视频/文档"、"微信文件去重"、"清理微信存储"、"删除微信重复文件"、"整理最近N个月的微信文件"时，必须使用本技能。自动检测微信文件目录（含电脑管家迁移路径），识别微信 (1)(2)(3) 括号命名重复文件，支持移到回收站、按月份+类型分类整理、按时间范围过滤，所有操作前必须 dry-run 预览并等待用户二次确认。
---
# 微信文件整理技能

## 功能概述

-   自动检测微信文件存储路径（含非默认迁移路径）
    
-   识别微信重复文件：普通重复 + 括号序号命名（`文件(1).pdf`、`文件(2).pdf`）
    
-   **重复文件移入回收站**（非永久删除，可恢复）
    
-   按月份+类型分类，复制到用户指定目录
    
-   支持 `--since` 时间范围过滤（如只整理最近3个月）
    
-   **两阶段确认**：dry-run 预览 → 用户确认 → 执行
    

* * *

## 执行流程

### 第一步：检测 / 读取配置

```bash
python scripts/detect_wechat_dir.py
```

脚本会输出当前状态，Agent 根据结果执行不同的后续操作：

**情况 A：已有配置文件（status = found\_config）**

脚本展示已保存的源目录、目标目录、上次整理时间。

-   询问用户：「沿用上次配置吗？（直接回复"是"，或输入"reset"重新配置）」
    
-   用户确认沿用 → 直接进入第三步
    
-   用户说 reset → 进入第二步重新配置
    

**情况 B：首次运行 / 检测到候选路径（status = found\_single / found\_multiple）**

-   若只有一个候选，向用户展示并询问确认：「检测到微信文件目录：\[路径\]，使用这个目录吗？」
    
-   若有多个候选，列出编号让用户选择
    
-   用户确认后 → 进入第二步
    

**情况 C：未检测到任何路径（status = not\_found）**

-   请用户手动输入源目录路径
    
-   确认路径存在后 → 进入第二步
    

**配置文件位置：skill 根目录下的** `config.json`  
（与 `SKILL.md` 同级，即 `.agents/skills/wechat-file-organizer/config.json`）

操作日志同样保存在 skill 根目录：`organizer_log.txt`

* * *

### 第二步：询问并保存配置

**仅在以下情况执行本步骤：首次运行、reset、或配置文件中缺少某项字段。**

需要收集并确认的字段：

1.  **source\_dir（微信源目录）**
    
    -   来自第一步检测结果或用户手动输入
        
    -   必须确认路径实际存在
        
2.  **dest\_dir（目标保存目录）**
    
    -   配置中无此字段 → 必须询问用户，提示默认值 `%USERPROFILE%\Documents\微信整理`
        
    -   用户可直接回车接受默认，或输入自定义路径
        
3.  **mode（分类方式，默认 month\_type）**
    
    -   `month_type`：按月份+类型，如 `2024-03/图片/`
        
    -   `type_only`：仅按类型，如 `图片/`
        
    -   `month_only`：仅按月份，如 `2024-03/`
        
    -   可以询问，也可以直接使用默认值，无需强制询问
        

收集完成后，用以下格式写入配置文件：

```python
import json
from pathlib import Path

config = {
    "source_dir": "<用户确认的源目录>",
    "dest_dir":   "<用户确认的目标目录>",
    "mode":       "month_type",
    "last_run":   None
}
# 配置文件放在 skill 根目录（与 SKILL.md 同级）
config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print(f"✅ 配置已保存到：{config_path}")
```

保存后告知用户配置文件的完整路径。

* * *

### 每次整理前：确认目标目录

**无论是否已有配置，每次执行整理操作前，都必须向用户展示目标目录并明确确认：**

> 「将整理到：`%USERPROFILE%\Documents\微信整理`，确认吗？（或输入新路径）」

-   用户确认 → 继续
    
-   用户输入新路径 → 更新配置文件中的 `dest_dir`，再继续
    

### 第三步：统一 Dry-run 预览（必须执行，不可跳过）

用一个命令同时展示「重复文件分析」+「整理后目录结构」：

```bash
python scripts/preview.py \
  --source "<源目录>" --dest "<目标目录>" \
  [--mode month_type] [--since YYYY-MM]
```

预览报告包含两部分：

```
📋 微信文件整理完整预览
══════════════════════════════════════════════════════════
源目录：D:\xxx\xwechat_files\wxid_xxx\msg\file
目标目录：D:\Documents\微信整理
分类模式：month_type    时间范围：2026-01 至今

─────────────────────────────────────────────────────────
🗑  Part 1 · 重复文件（将移入回收站）
─────────────────────────────────────────────────────────
  发现重复组：32 组  →  将移入回收站：74 个文件（节省 197 MB）
    括号序号重复：28 组（如 文件(2).pdf）
    完全相同重复：4 组

  月份         重复文件数       节省空间
  ------------ ---------- ------------
  2026-01             12 个      45.3 MB
  2026-02             35 个      98.1 MB
  2026-03             27 个      53.6 MB

  示例（前15组）：
  保留                                 移除（→回收站）
  文件.pdf                          ❌ 文件(2).pdf  (9.8 MB)
  report.html                       ❌ report(2).html  (60 KB)
  ...

─────────────────────────────────────────────────────────
📂 Part 2 · 整理后目录结构（将复制到目标目录）
─────────────────────────────────────────────────────────
  待整理文件：109 个（共 293 MB）

  文件类型分布：
    文档    64 个  ████████████████
    其他    35 个  ████████
    压缩包   9 个  ██
    音频     1 个  

  目标目录结构：
    D:\Documents\微信整理\2026-01\文档\  → 15 个文件 · 120 MB
    D:\Documents\微信整理\2026-02\文档\  → 28 个文件 · 89 MB
    ...

══════════════════════════════════════════════════════════
📌 操作建议
══════════════════════════════════════════════════════════
  步骤 A · 清理重复文件 → 将 74 个文件移入回收站（释放 197 MB）
  步骤 B · 整理文件到目标目录 → 复制 109 个文件

⚠️  以上为完整预览，确认后请告知执行哪些步骤。
```

若用户只想做去重或只想整理，可以只执行步骤 A 或步骤 B。

### 第四步：**等待用户明确确认**

展示 dry-run 报告后，**必须明确询问用户是否执行**，不得自动继续。

示例确认语：「以上是预览结果，确认执行吗？」

### 第五步：执行

用户确认后，分步执行（可选择只做其中一步）：

```bash
# 步骤A：清理重复文件（移入回收站）
python scripts/dedup_recycle.py --source "<源目录>"

# 步骤B：整理文件到目标目录
python scripts/scan_and_organize.py \
  --source "<源目录>" --dest "<目标目录>" \
  --mode <模式> [--since YYYY-MM]
```

执行日志追加写入 `~/.wechat_organizer_log.txt`。

* * *

## 去重规则（重要）

### 两类重复的识别方式

**A. 括号序号重复**（微信自动命名）：

-   识别 `文件名 (N).ext` 格式（N 为数字）
    
-   提取基础名：`文件名.ext`
    
-   将相同基础名、**相同大小**的归为一组
    
-   ⚠️ **大小不同则不视为重复**（可能是真的不同版本）
    

**B. 完全相同重复**：

-   文件名完全相同 + 文件大小完全相同
    

### 保留策略

-   每组中保留**修改时间最新**的文件
    
-   **原始文件名优先**：若最新的文件是 `(N)` 版本，则在移动到目标目录时，将其重命名为不带括号的基础名
    
-   其余重复文件**移入回收站**（非永久删除）
    

### 不同名、不同大小 = 不是重复

`report.html` 和 `report_v2.html` 不会被误判为重复，即使基础名相似。

* * *

## 文件类型分类规则

<table style="min-width: 50px;"><colgroup><col style="min-width: 25px;"><col style="min-width: 25px;"></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>类型</p></th><th colspan="1" rowspan="1"><p>扩展名</p></th></tr><tr><td colspan="1" rowspan="1"><p>图片</p></td><td colspan="1" rowspan="1"><p>jpg, jpeg, png, gif, webp, bmp, heic, tiff, svg</p></td></tr><tr><td colspan="1" rowspan="1"><p>视频</p></td><td colspan="1" rowspan="1"><p>mp4, avi, mov, mkv, wmv, flv, m4v, 3gp, rmvb</p></td></tr><tr><td colspan="1" rowspan="1"><p>音频</p></td><td colspan="1" rowspan="1"><p>mp3, wav, aac, m4a, ogg, opus, amr, flac, wma</p></td></tr><tr><td colspan="1" rowspan="1"><p>文档</p></td><td colspan="1" rowspan="1"><p>pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, md, rtf</p></td></tr><tr><td colspan="1" rowspan="1"><p>压缩包</p></td><td colspan="1" rowspan="1"><p>zip, rar, 7z, tar, gz, bz2, xz</p></td></tr><tr><td colspan="1" rowspan="1"><p>其他</p></td><td colspan="1" rowspan="1"><p>以上未覆盖的文件（html, json, py, sql 等）</p></td></tr></tbody></table>

* * *

## \--since 时间范围参数

`--since YYYY-MM` 表示只处理该月份及之后的文件（按文件修改时间）。

示例：

```bash
# 只整理最近3个月（从2026-01起）
python scripts/scan_and_organize.py --source ... --dest ... --since 2026-01

# 整理所有文件（不传 --since）
python scripts/scan_and_organize.py --source ... --dest ...
```

Agent 收到"最近N个月"的指令时，自动计算起始月份并传入 `--since`。

* * *

## 配置文件

保存在 `~/.wechat_organizer_config.json`：

```json
{
  "source_dir": "D:\\电脑管家迁移文件\\xwechat_files\\wxid_xxx\\msg\\file",
  "dest_dir": "D:\\Documents\\微信整理",
  "mode": "month_type",
  "last_run": "2026-03-29 14:00:00"
}
```

* * *

## 脚本说明

<table style="min-width: 50px;"><colgroup><col style="min-width: 25px;"><col style="min-width: 25px;"></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>脚本</p></th><th colspan="1" rowspan="1"><p>用途</p></th></tr><tr><td colspan="1" rowspan="1"><p><code>scripts/detect_wechat_dir.py</code></p></td><td colspan="1" rowspan="1"><p>检测微信文件目录（含电脑管家迁移路径）</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>scripts/preview.py</code></p></td><td colspan="1" rowspan="1"><p><strong>统一预览</strong>：同时展示去重分析 + 整理结构，不执行任何操作</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>scripts/dedup_recycle.py</code></p></td><td colspan="1" rowspan="1"><p>去重并将重复文件移入回收站（支持 <code>--dry-run</code>）</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>scripts/scan_and_organize.py</code></p></td><td colspan="1" rowspan="1"><p>扫描、分类、复制到目标目录（支持 <code>--dry-run</code>、<code>--since</code>）</p></td></tr></tbody></table>

**标准使用顺序：**

1.  `detect_wechat_dir.py` → 确认路径
    
2.  `preview.py` → 查看完整预览
    
3.  用户确认后 → `dedup_recycle.py`（可选）+ `scan_and_organize.py`