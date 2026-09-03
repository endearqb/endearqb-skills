---
name: product-story-pptx
description: 创建并迭代产品展示、产品介绍、产品发布、功能演示、解决方案路演与 Demo Day 类图文 PPTX。当用户要求有情绪起伏的叙事、full/half/edge bleed 图片版式、可编辑 UI mockup、有审美的流程图或架构图、遵循 Storytelling with Data 的图表、避免模板味或 AI 味时使用。覆盖 brief、Big Idea、三幕故事、主题篇幅预算、逐页 energy/mood、deck spec、版本 lineage、机器 lint、python-pptx 生成、渲染巡检与结构 QA。可从零创建，也可继续维护具备 spec、脚本、manifest 等源文件的同构项目；只有任意既有 PPTX 或客户模板而无可重建源文件时，请改用通用 PPTX 编辑技能。
license: MIT
metadata:
  version: "1.2.0"
---

# product-story-pptx

把产品讲成一段有蓄力、转折、证明与召唤的故事，再把故事落成一份可编辑、可验证的 `.pptx`。

这不是“把要点填进模板”的技能。固定顺序是：

1. 先定受众、行动与 Big Idea。
2. 再定三幕结构、每页 energy 与 mood。
3. 再选页面 type、bleed 与视觉素材。
4. 写成机器可读的 `spec.yaml`。
5. 运行 lint，0 FAIL 后才生成。
6. 渲染、肉眼检查、结构检查，至少修正一轮。
7. 交付版本化 deck、lineage manifest、预览和待替换素材清单。

## 适用边界

使用本技能：

- 产品发布、产品介绍、销售方案、解决方案路演、Demo Day、功能发布。
- 需要真实产品图、界面截图、场景图与数据图表共同讲故事。
- 需要控制情绪节奏，而不是平均用力。
- 需要可复现的代码生成与机器门禁。
- 已有本 skill 生成或结构兼容的 source project，需要根据截图、逐页反馈继续多轮迭代。

不要使用本技能：

- 只有既有 `.pptx` 而没有 spec、脚本或 manifest 的逆向修改；套用客户模板、合并拆分幻灯片。
- 大量表格型经营报表、培训讲义、逐字教材。
- 用户只要大纲、讲稿或一张静态信息图。

## 输出契约

每个项目至少生成：

```text
ppt-project-<slug>/
├── brief.md
├── outline.md
├── spec.yaml
├── assets/
├── out/
│   ├── <name>.pptx
│   ├── <name>.manifest.json
│   └── <name>_preview/
│       ├── <name>.pdf
│       ├── slide-01.png ...
│       └── contact_sheet.png
└── validation.md
```

迭代项目保留父 manifest，并用新版本文件名输出；不得覆盖唯一可工作的上版。

交付时同时说明：

- Big Idea 与三幕故事线。
- energy 序列及主要峰谷。
- 示例数据、合成占位图、字体依赖等仍需替换的内容。
- lint 与 inspect 的真实结果；不得口头宣布通过。

## 三条设计信念

1. **情绪先于版式。** 每页先决定 `energy: 1–5` 与 `mood`，再选择版式；版式是情绪的载体。
2. **图片是一等公民，bleed 是节奏工具。** 满版大图用于峰值、转场和呼吸，不是默认背景。
3. **数据为结论服务。** 每张图先有 action title，再有图；先灰后亮、去除杂乱、直接标注、明确来源。

## 资源路由

只在当前阶段读取必要文件，不要一次加载全部参考资料。

| 阶段 | 必读文件 | 目的 |
|---|---|---|
| 需求与故事 | `references/narrative-arc.md` | Big Idea、三幕结构、energy/mood |
| 逐页编排 | `references/layout-system.md` | type、网格、密度与页面节奏 |
| 图片页 | `references/bleed-layouts.md` | bleed、裁切、scrim、图片门槛 |
| 流程/架构 | `references/diagram-patterns.md` | 图形拓扑、节点与高亮规则 |
| 图表/数字 | `references/data-storytelling.md` | SWD 图表选择、聚焦与来源 |
| 视觉方向 | `references/visual-language.md` | 主题、字体、颜色、图像风格 |
| 生成后 QA | `references/qa-checklist.md` | lint、inspect、肉眼巡检闭环 |
| 多轮迭代 | `references/iteration-lineage.md` | source project 识别、版本谱系与回归范围 |
| UI 示意 | `references/editable-ui-mockups.md` | 可编辑公共组件、几何不变量与重复实例 QA |
| 理解设计来源 | `references/research-basis.md` | Claude/Codex/GitHub/SWD 调研 |
| 文件总索引 | `references/INDEX.md` | 文件职责与扩展入口 |

## 工作流

### Stage 0 · 恢复现场或新建项目

如果已有项目目录，先读 `references/iteration-lineage.md`，检查 `brief.md`、`outline.md`、`spec.yaml`、生成脚本、PPTX、manifest 与预览是否存在，从最近的未通过门禁处继续。不要重新猜测已经确认的受众、品牌与故事线。

已有 source project 的本轮修改先建立 change map：用户反馈 → 目标页 → 公共组件 → 受影响的全部实例 → 回归页。截图中的标注是审阅证据，不是 deck 内容。若只存在 PPTX 而没有可重建源文件，停止使用本 skill 并转通用 PPTX 编辑工作流。

新项目创建工作目录，并复制模板：

```bash
mkdir -p ppt-project-<slug>/{assets,out}
cp assets/example-deck-spec.yaml ppt-project-<slug>/spec.yaml
```

### Stage 1 · 写 brief

只在缺失会改变整份 deck 方向时提问，一次问完关键项：

- 产品是什么，解决什么高代价问题。
- 观众是谁，谁拥有决策权。
- 场合、时长、屏幕与交付日期。
- 看完后希望观众采取什么具体行动。
- 可用的产品图、截图、数据、证言、品牌色与字体。
- 必须出现或禁止出现的内容。
- 主题篇幅预算，例如主线、行业专题或能力分支最多/最少占全篇多少。

在 `brief.md` 中写：

```markdown
# Brief
- Product:
- Audience:
- Decision context:
- Desired action:
- Duration / target slides:
- Big Idea:
- Available evidence:
- Available visuals:
- Brand constraints:
- Non-negotiables:
- Topic budgets:
- Assumptions / placeholders:
```

Big Idea 必须是一句完整主张，包含“独特观点 + 对观众的利害关系”。

### Stage 2 · 设计故事与情绪曲线

读 `references/narrative-arc.md`，输出三幕：

1. 现状与裂缝：建立共同处境和代价。
2. 转折与方案：揭示产品如何改变机制。
3. 证明与召唤：用证据建立信任，并要求行动。

然后在 `outline.md` 逐页写：

```text
页码 | act | type | bleed | energy/mood | action title | visual/evidence | notes purpose
```

先看 energy 序列是否成立，再写正文。至少满足：

- 开场 `energy >= 3`。
- 前 30% 内出现一次 `energy <= 2` 的低谷。
- 最后两页至少一页为 `energy = 5`。
- 不连续 3 页 energy 相同。
- `max(energy) - min(energy) >= 2`。
- 高峰前有收紧或低谷，不连续轰炸观众。

### Stage 3 · 规划视觉资产

为每页标记视觉责任：真实产品图、界面截图、场景图、图表、流程图、对照或纯文字换气页。

需要展示产品界面但缺少可用截图时，读 `references/editable-ui-mockups.md`，用 `ui_mockup` 公共组件生成可编辑原生形状，并明确标注“界面示意”。有 3–5 个并列条目且每条都需要专属图片时，使用 `media_bars`；小图必须根据所属条目的具体内容选择或生成，不得复用无关装饰图。

缺图时按以下顺序处理：

1. 请求真实产品图或截图。
2. 用 `color-block` 或大字 statement 承担峰值。
3. 生成明确标注为“合成占位”的示意图。
4. 最后才考虑高质量图库图；禁止用握手、灯泡、齿轮、假笑会议等陈词滥调凑数。

图片不得拉伸。所有照片与截图通过 `image_focus` 做 cover 裁切。

### Stage 4 · 写 `spec.yaml`

读 `assets/example-deck-spec.yaml`、`assets/layout-registry.yaml` 与所需参考文档。

顶层 `deck` 必须包含：

- `title`
- `big_idea`
- `audience`
- `desired_action`
- `theme`
- `language`
- `assets_dir`

多轮迭代在 `deck.lineage` 中记录 `mode`、`version`、`parent_manifest`、`change_summary`、`regression_pages` 与 `affected_components`。需要限制主题篇幅时，写 `deck.topic_budgets`，并用各页 `topics` 标记归属。

每页必须包含：

- `type`
- `bleed`
- `energy`
- `mood`
- `title`

action title 要说结论，不要只写“产品介绍”“市场规模”“解决方案”。中文标题不超过 24 字，英文不超过 14 词。

### Stage 5 · 内容门禁

运行：

```bash
python scripts/lint_deck.py ppt-project-<slug>/spec.yaml
```

只有 **0 FAIL** 才能生成。WARN 必须逐条判断，不得默认忽略。Lint 检查：

- schema、主题与 type↔bleed 兼容。
- action title 与文字预算。
- energy 曲线与 bleed 预算。
- full/overlay 图片、分辨率与 scrim。
- 上下半屏 bleed、UI mockup 和 media bars 字段完整性。
- 图表类型、highlight、source 与示例数据标注。
- 流程图节点数、单一高亮与标签长度。
- 连续图表页和重复版式。
- closing 与 CTA。
- 主题篇幅预算、版本 lineage 与回归页有效性。

### Stage 6 · 生成、渲染与双重 QA

生成：

```bash
python scripts/build_deck.py \
  ppt-project-<slug>/spec.yaml \
  ppt-project-<slug>/out/<name>.pptx
```

渲染：

```bash
python scripts/render_preview.py \
  ppt-project-<slug>/out/<name>.pptx \
  --dpi 120 --cols 4
```

结构检查：

```bash
python scripts/inspect_pptx.py \
  ppt-project-<slug>/out/<name>.pptx
```

必须同时满足：

- lint：0 FAIL。
- inspect：0 ERROR。
- 已打开 `contact_sheet.png` 看完整体节奏。
- 已逐页看过所有 PNG，检查裁切、对比度、溢出、对齐、图表重点与流程图阅读顺序。
- UI mockup 的 shell、标题栏、divider 形成整体；所有重复实例的圆角、标题栏高度和内边距一致。
- iteration 指定的回归页、所有受影响组件实例及其相邻页均已复核。
- 至少完成一次“改 spec → lint → build → render → inspect”修正循环。

只改 `spec.yaml`、tokens、registry 或脚本；不要手工修改生成后的 PPTX，否则下一次构建会覆盖且无法复现。

### Stage 7 · 交付

交付：

- `.pptx`
- `.manifest.json`
- `contact_sheet.png`
- `validation.md`
- 必要时附 PDF

交付说明包含 3–5 句故事线、energy 序列、数据来源状况、待替换资产和已知限制。

迭代交付还应说明：父版本、change summary、回归页、公共组件影响面，以及哪些上轮问题已确认没有复发。

## 硬规则

1. 每页一句 action title；中文 ≤ 24 字，英文 ≤ 14 词。
2. `full + color-block` 页数不超过全篇 40%；不得连续 3 页 full。
3. 至少使用 3 种 bleed 模式，且必须包含 `none`。
4. full/overlay 必须有图、有 scrim；满版图宽度至少 1920 px。
5. 压图页 title + body 中文合计 ≤ 24 字，英文 ≤ 12 词。
6. 连续 `chart/big_number` 不超过 2 页；之后用 statement、section、quote 或 feature hero 换气。
7. 图表只用 `bar / hbar / line / slope / dot`；禁止饼图、环图、3D、双轴和装饰性雷达图。
8. 柱状图从 0 开始；每图高亮不超过 2 项；`source` 必填；示例数据必须显式标注。
9. 流程图 3–7 个节点、恰好一个高亮、单一方向；label ≤ 6 汉字或 3 词。
10. 正文 ≤ 60 字；bullets ≤ 4 条，每条 ≤ 20 字；每页视觉单元不超过 5 个。
11. 最多两族字体加一个 CJK 回退；强调色只表达重点、当前步骤或 CTA。
12. 图片 cover 裁切不拉伸；全篇色调与光线方向一致。
13. 不以“自动缩小字号”解决内容过量；先删字、拆页或换版式。
14. 最后一页不是“谢谢”，而是明确的新常态或行动召唤。
15. 未运行门禁脚本、未读取输出时，不得声称通过。
16. `ui_mockup` 必须使用公共 renderer、保留关键 shape name、标注“界面示意”，并通过外框几何与重复实例 QA。
17. `media_bars` 必须 3–5 条、每条一张语义匹配图片；文字 bar 默认约占 60%，但不得把 60% 写死为所有 deck 的唯一比例。
18. 主题篇幅用 `topic_budgets` 约束，不把某个项目的 10–15% 等具体数值固化为通用规则。
19. 每次 iteration 都保留父 manifest、生成新版本，并重新 lint/build/render/inspect；上轮通过不等于本轮通过。

## Fast Track

仅当同时满足以下条件时，可压缩 Stage 2–4 的文档量：

- 总页数 ≤ 5。
- 无数据图表或复杂流程图。
- 用户明确要求快速、简单或临时演示。

仍然必须完成：brief、lint、build、render、inspect 与肉眼 QA。

## 主题与扩展

- 在 `assets/design-tokens.yaml` 新增主题，不要把颜色散落在脚本里。
- 在 `assets/layout-registry.yaml` 新增 type/bleed 组合和坐标，不要在 builder 中随意硬编码。
- 图表规则在 `scripts/chart_swd.py` 与 `references/data-storytelling.md` 同步更新。
- 流程图样式在 `scripts/flow_diagram.py` 与 `references/diagram-patterns.md` 同步更新。
- 任何跨项目可复现的修正，应写入相应 reference 或 lint 规则，而不是只在对话里记住。

## 环境与自检

安装：

```bash
python -m pip install -r requirements.txt
```

视觉 QA 还需：

```bash
# macOS
brew install --cask libreoffice
brew install poppler

# Ubuntu / Debian
sudo apt install libreoffice-impress poppler-utils
```

完整自检：

```bash
python scripts/smoke_test.py
```

自检只有在所有 Python 编译、YAML 解析、lint、build、inspect 与 render 全部通过时才返回 0。
