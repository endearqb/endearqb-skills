---
name: community-profiler
metadata:
  version: 4.1.0
description: >
  技术讨论群成员画像与评估 Skill。当用户提供群聊记录（文本粘贴、截图、JSON/CSV 均可）并要求分析成员、给成员打分、评估社区健康度、
  找出核心贡献者/潜水者/活跃用户/KOL、生成成员影响力排名、识别僵尸用户、分析群运营健康度、总结群聊内容等时，必须触发本 Skill。
  适用场景：运营决策（KOL筛选、低价值成员风险评估）、个人研究（社区生态分析）、团队协作管理（成员贡献评估）。
  触发关键词：群画像、成员分析、社区分析、影响力评估、活跃度分析、群运营分析、KOL识别、技术贡献者分析、群聊记录分析、僵尸用户、聊天总结。
  即使用户只说"帮我分析一下这个群"或"看看谁最活跃"或"总结一下群里聊了什么"，也应触发本 Skill。
---

# Community Profiler v4.1.0 — 技术社区成员画像与评估

## 概述

将群聊记录解析为结构化成员画像，支持三种使用场景：
- **运营决策**：KOL 筛选、低价值成员风险评分
- **个人研究**：社区生态与知识流动分析
- **团队协作**：成员贡献与角色识别

---

## 输出架构（JSON + Viewer 分离）

本技能采用 **数据与视图分离** 架构：

### 输出文件
1. `report.json` — AI 分析结果的唯一结构化输出（**必须**）
2. `viewer.html` — 从 `assets/viewer.html` 复制到输出目录的独立可视化查看器（**自动**）
3. `report.md` — 文字分析报告（仅用户明确要求时）
4. `assets/` — 抓取的链接/图片内容（有外部资源时）

### 输出流程（严格按此顺序）

```
Step A：分析群聊 → 生成 report.json → 保存到输出目录
Step B：从技能 assets/ 复制 viewer.html 到输出目录（与 report.json 同级）
Step C：使用 present_files 将 viewer.html（第一个）和 report.json 呈现给用户
```

### 关键命令序列

```bash
# 1. 创建输出目录
OUTPUT_DIR="/mnt/user-data/outputs/groupchat/$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 2. 保存 report.json（由 AI 分析生成，用 create_file 写入）
# → $OUTPUT_DIR/report.json

# 3. 复制 viewer.html 到输出目录
cp /mnt/skills/user/community-profiler/assets/viewer.html "$OUTPUT_DIR/viewer.html"

# 4. 通过 present_files 呈现给用户
# present_files(["$OUTPUT_DIR/viewer.html", "$OUTPUT_DIR/report.json"])
```

> ⚠️ **重要**：viewer.html 和 report.json 必须在同一目录下。viewer.html 通过 `fetch('./report.json')` 自动加载数据。

所有文件保存至 `groupchat/YYYY-MM-DD_HHMMSS/`（按分析时间戳新建）。

---

## Step 0：规模判断与预处理策略

**首先判断消息量级，选择对应工作流：**

| 规模 | 消息数 | 策略 |
|------|--------|------|
| 小型 | < 200 条 | 全量分析，一次性输出 |
| 中型 | 200-1000 条 | 分块分析（每块200条），subagent 资产抓取与主分析**并行** |
| 大型 | > 1000 条 | 分块分析 + 向用户报告进度，HTML 启用虚拟滚动 |

### 0.1 广告/垃圾信息过滤

标记为 `spam`，不计入评分：
- 营销话术（购买/优惠/引流）
- 同一人 3 条内容相似度 > 80%
- 连续 5 条以上纯表情包
- 短链 + 邀请码格式

### 0.2 Bot 识别排除

排除昵称含 Bot/助手/机器人/通知/公告 或发言模式高度规律的账号，单独列出。

### 0.3 无时间戳处理

无时间戳时：时序子项跳过，权重自动切换：
- 有时间戳：活跃度20% · 内容质量30% · 互动影响25% · 专业权威15% · 社区粘性10%
- 无时间戳：活跃度15% · 内容质量35% · 互动影响30% · 专业权威20% · 社区粘性0%

---

## Step 1：解析输入

| 格式 | 处理 |
|------|------|
| 微信/TG/Slack/Discord 导出文本 | 解析时间戳、昵称、消息 |
| 截图 | OCR 后按文本处理 |
| JSON / CSV | 直接读取字段映射 |
| 多文件/分段粘贴 | 合并去重 |

字段缺失时：说明缺失内容，继续最佳估计，不中止。

---

## Step 2：外部资源抓取（Subagent 并行）

**与主分析流程并行执行，不阻塞成员评分。**

### 去重与优先级

- 按 URL/图片 hash 去重，只抓取一次，累计 `share_count`
- 优先：技术文章/文档/仓库/被 ≥3 人提及的链接
- 低优先：社交主页、电商页

### 失败处理

| 原因 | 标注 |
|------|------|
| 403/401 | `failed_403` |
| 超时 >10s | `failed_timeout` |
| 付费墙 | `failed_paywall` |
| 404 | `dead_link` |

### 保存结构

```
assets/
├── index.json       # 资产清单
├── articles/        # 文章摘要（.md）
├── images/          # 重要图片
└── repos/           # 仓库信息
```

---

## Step 3：五维画像评分

> 💡 **权重扩展点**：所有权重集中于 Step 0.3，后续迭代可在此添加自定义逻辑。

### 维度一：活跃度
```
= min(100, 发言数/全体中位数×50 + 活跃天数占比×30[无时间戳=0] + 跨话题参与度×20)
```
发言 < 3 条上限 30。

### 维度二：内容质量（抽样最多20条）

| 子维度 | 高分信号 | 满分 |
|--------|---------|------|
| 技术深度 | 原理/源码/架构 | 25 |
| 信息密度 | 干货多、信息量高 | 25 |
| 原创性 | 个人观点、独立分析 | 25 |
| 表达清晰度 | 逻辑清晰、易读 | 25 |

发言 < 5 条标注 `sample_insufficient`。

### 维度三：互动影响力
```
原始分 = 被@数×3 + 引发回复数×2 + 主动回复数×1
→ 归一化到 0-100
```

### 维度四：专业权威

以下信号各 +20，上限 100：
✅ 解答技术问题被采纳 ✅ 给出可执行代码/方案 ✅ 纠正错误信息 ✅ 被他人引用认可 ✅ 分享资源 share_count ≥ 3

### 维度五：社区粘性（无时间戳时跳过）
```
= 连续活跃周数/总周数×50 + 跨话题参与数/总话题数×50
```

---

## Step 4：角色分类

| 角色 | 判定 |
|------|------|
| 🎯 核心贡献者 | 综合≥70，内容质量≥70，权威≥60 |
| 🔧 问题解决者 | 权威≥70，回复他人占互动>60% |
| 📢 信息传播者 | 活跃高，原创性<40，链接/转发>50% |
| ❓ 优质提问者 | 引发回复前25%，权威<40 |
| 👀 潜水观察者 | 活跃<20，发言<5条 |
| 😄 氛围组 | 活跃高，内容质量<40，水文为主 |
| 🌱 新人成长者 | 发言少但提问多、积极互动 |
| ⚠️ 低贡献风险 | 活跃<10，内容质量<20，无有效互动 |

---

## Step 5：聊天内容总结

在完成成员评分后，对全量消息进行一次内容层面的分析，输出到 JSON 的 `content_summary` 字段。

### 5.1 核心议题摘要

识别 3-8 个主要话题线程，每个包含：
- 议题标题（10字以内）
- 简述（2-3句，覆盖主要观点）
- 参与者列表
- 议题热度（参与人数 + 消息数）

### 5.2 精华发言精选

选取 5-10 条最有价值的发言，标准：
- 引发 ≥3 条回复
- 包含可操作的技术方案
- 提出了有洞察力的问题或反驳
- 被他人引用或认可

每条保留原文（不改写）+ 发言人 + 价值标注。

### 5.3 共识与分歧

- **共识**：多人达成一致的观点（≥3人明确认同）
- **分歧**：存在明确对立观点的议题，列出双方核心论点

### 5.4 行动项 / 待办

提取群内有人明确提出的计划、建议、邀约等，格式：
```
- [提出人] 行动内容 （对象：涉及人）
```

---

## Step 6：运营决策支持

### A. KOL 筛选
输出 `kol_candidates`，包含推荐理由和适用场景。

### B. 低价值成员风险评分
**只输出风险评分（0-100）和风险因素，不输出清退名单。**
- `high`（≥70）/ `medium`（40-69）/ `low`（<40）

### C. 团队协作
- 知识覆盖矩阵（covered/weak/gap）
- 核心-外围三层分层
- 互动断层识别

---

## Step 7：输出 report.json

### 完整 JSON 结构

```json
{
  "analysis_meta": {
    "generated_at": "2025-05-14 12:00:00",
    "total_messages": 150,
    "member_count": 12,
    "spam_messages_filtered": 5,
    "has_timestamp": true,
    "weight_mode": "standard",
    "source_format": "wechat_text",
    "bots_excluded": []
  },
  "content_summary": {
    "topics": [
      {
        "title": "议题标题",
        "description": "2-3句描述",
        "participants": ["昵称"],
        "message_count": 12,
        "heat_score": 85
      }
    ],
    "highlights": [
      {
        "sender": "昵称",
        "content": "原文",
        "value_tag": "技术洞察|精准提问|有效解答|引发讨论",
        "replies_triggered": 4
      }
    ],
    "consensus": ["共识观点1", "共识观点2"],
    "disputes": [
      {
        "topic": "争议议题",
        "side_a": { "position": "观点A", "supporters": ["昵称"] },
        "side_b": { "position": "观点B", "supporters": ["昵称"] }
      }
    ],
    "action_items": [
      { "proposer": "昵称", "action": "行动内容", "target": "涉及对象" }
    ]
  },
  "members": [
    {
      "nickname": "成员昵称",
      "scores": {
        "composite": 75,
        "activity": 60,
        "content_quality": 80,
        "interaction_influence": 70,
        "professional_authority": 85,
        "community_stickiness": 50
      },
      "roles": ["🎯 核心贡献者"],
      "churn_risk_level": "low",
      "risk_factors": [],
      "highlights": ["代表性发言原文"],
      "tech_domains": ["Go", "Docker"],
      "stats": {
        "message_count": 25,
        "reply_count": 10,
        "mentioned_count": 5,
        "links_shared": 3,
        "active_days": 7
      }
    }
  ],
  "community_health": {
    "kol_candidates": [
      {
        "nickname": "昵称",
        "composite_score": 85,
        "kol_signals": ["高内容质量", "被多人 @ 引用"],
        "tech_domains": ["AI", "Python"],
        "recommended_for": "技术分享嘉宾"
      }
    ],
    "risk_summary": { "high": 2, "medium": 3, "low": 7 },
    "knowledge_coverage": {
      "领域名": { "level": "covered|weak|gap", "experts": ["昵称"] }
    },
    "core_periphery_layers": {
      "core": ["核心成员"],
      "active": ["活跃成员"],
      "peripheral": ["边缘成员"]
    },
    "topic_clusters": ["话题1", "话题2"],
    "activity_trend": "上升|稳定|下降",
    "top_assets": [
      {
        "title": "资源标题",
        "url": "https://example.com",
        "summary": "资源摘要",
        "share_count": 3,
        "shared_by": ["昵称A", "昵称B"],
        "fetch_status": "success|failed_403|failed_timeout|failed_paywall|dead_link"
      }
    ],
    "health_notes": "社区健康评估文字描述"
  },
  "failed_assets": []
}
```

### top_assets 字段约束

- `top_assets` 为空时必须输出 `[]`。
- `top_assets[].shared_by` 必须始终是字符串数组；没有可识别分享者时输出 `[]`，不要输出字符串。
- 抓取失败但仍值得展示的资源可以保留在 `top_assets` 中，并用非 `success` 的 `fetch_status` 标注。
- `failed_assets` 保留为原始失败清单，供审计和调试使用；当前 `viewer.html` 不直接渲染该字段。

---

## Step 8：部署 Viewer 并呈现给用户

完成 report.json 后，**必须**执行以下操作：

```bash
# 复制 viewer.html 到输出目录
cp /mnt/skills/user/community-profiler/assets/viewer.html "$OUTPUT_DIR/viewer.html"
```

然后使用 `present_files` 工具呈现文件，**viewer.html 优先作为第一个文件**：

```python
present_files(["$OUTPUT_DIR/viewer.html", "$OUTPUT_DIR/report.json"])
```

### Viewer 工作原理

`assets/viewer.html` 是一个独立的可视化报告查看器，直接消费 `report.json`：
- **自动加载**：通过 `fetch('./report.json')` 加载同目录的数据文件
- **URL 参数**：支持 `?data=路径` 指定不同 JSON 文件
- **文件上传回退**：若 fetch 失败，显示文件选择器供手动上传 JSON
- **主题切换**：支持 light/dark 主题切换
- **导出功能**：可重新导出当前加载的 JSON 数据
- **成员排行**：按 `members[].scores.composite` 排序，展示前三名、完整成员列表和五维雷达图
- **详情展开**：成员列表点击后展开五维评分、代表发言、技术领域、统计数据和风险因素
- **运营面板**：展示 KOL 候选、风险分布、知识覆盖、角色分布、活跃度分布和社区健康结论
- **资源热榜**：展示 `community_health.top_assets`，其中 `shared_by` 按数组渲染为分享者列表

### ⚠️ 不要自行生成 HTML 报告

与 v3 版本不同，**不再需要**在 AI 输出中生成完整 HTML。viewer.html 是预置的静态资产，只需复制到输出目录即可。AI 只负责生成 report.json 数据。

---

## Step 9：Markdown 报告（可选）

仅用户明确要求时生成，新增"聊天内容总结"章节作为第二节。

---

## 边界处理

| 情况 | 处理 |
|------|------|
| 记录 < 10 条 | 提示数据不足，仍输出最佳估计 |
| 只有 1-2 人 | 说明无法做比较分析 |
| 无时间戳 | Step 0.3 自动切换 |
| 非技术群 | "专业权威"改"领域权威"，向用户说明 |
| 时区未知 | 默认 UTC+8 |
| 大型记录 > 1000 条 | 启用分块处理，viewer 已内置虚拟滚动 |

---

## 参考文件

- `assets/viewer.html` — 独立可视化报告查看器，自动加载并渲染同目录 `report.json`
- `references/scoring-examples.md` — 各维度典型评分案例
