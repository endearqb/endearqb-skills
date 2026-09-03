# 调研依据与设计决策

> Skill 路径：`product-story-pptx/references/research-basis.md`
>
> 快照日期：2026-09-02。GitHub star 会变化，本表只用于说明调研时的社区热度，不代表质量排名。

## 1. 结论

本 skill 不是从某一个仓库复制而来，而是把四类实践重新组合：

1. Agent Skills 的渐进披露结构。
2. 官方 PPTX 技能的“生成后必须验证与看图”纪律。
3. 社区 slide skills 的结构化门禁、风格先行与 hero/non-hero 节奏。
4. Storytelling with Data 与 Duarte 的数据聚焦、对比和情绪弧原则。

最终选择：

- `SKILL.md` 保持短而可路由。
- 详细知识拆进 `references/`。
- 坐标与主题拆进 YAML。
- 可判断规则进入 lint/inspect。
- 生成后必须渲染，不允许只检查代码。
- 从零创建使用 python-pptx；当前图表用 Matplotlib PNG 保证样式稳定，流程图保持原生可编辑形状。

## 2. 官方技能规范

### Agent Skills specification

来源：

- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices
- https://agentskills.io/skill-creation/using-scripts

借鉴：

- 根目录必须有 `SKILL.md`，含 YAML frontmatter 与 Markdown 指令。
- `scripts/`、`references/`、`assets/` 按需加载。
- `SKILL.md` 应控制在 500 行以内，详细资料外置。
- 文件引用使用相对 skill 根目录路径。
- 脚本应有明确输入、输出、退出码与失败处理。

本实现：

- `SKILL.md` 约 300 行，只保留工作流与硬规则。
- `references/INDEX.md` 负责知识路由。
- 所有命令均从 skill 根目录执行。
- `smoke_test.py` 验证文件之间没有漂移。

### OpenAI Codex skills

来源：

- https://developers.openai.com/codex/build-skills
- https://developers.openai.com/codex/learn/best-practices

借鉴：

- Skill 是指令、资源和可选脚本的组合。
- 个人 skills 可放在 `$HOME/.agents/skills`，团队 skills 可提交到仓库 `.agents/skills`。
- `agents/openai.yaml` 可提供 display name、简述和默认 prompt。

本实现：

- 提供 `agents/openai.yaml`。
- 不声明 MCP 依赖。
- 安装文档同时覆盖个人与仓库级用法。

### Anthropic skills 与官方 PPTX skill

来源：

- https://github.com/anthropics/skills
- https://github.com/anthropics/skills/tree/main/skills/pptx

借鉴：

- 对 PPTX 任务区分“创建、编辑、读取”。
- 生成后运行结构验证。
- 通过缩略图和全分辨率渲染做视觉 QA。
- 明确说明库的 footguns，而不是假设生成一定正确。

差异：

- Anthropic 官方技能当前更偏通用 PPTX，并为新建 deck 推荐 PptxGenJS。
- 本 skill 是窄域的产品故事 deck，使用 python-pptx + YAML spec，强化情绪曲线、bleed 与 SWD 图表。
- 修改既有模板仍应交给通用 PPTX 技能。

## 3. GitHub 高热度与代表性项目

| 项目 | 2026-09-02 stars | 主要特征 | 本 skill 借鉴 |
|---|---:|---|---|
| [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 28,582 | 用前端能力创建网页 slides | 风格先行、把页面当完整视觉画布 |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 25,474 | 杂志/瑞士风、WebGL、演讲模式 | hero/non-hero 节奏、叙事弧、图片一等公民 |
| [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) | 832 | 学术演示、action title、证据纪律 | 强制论点式标题、结构化论证 |
| [addsumtech/slides_maker](https://github.com/addsumtech/slides_maker) | 492 | 可编辑 PPTX、原生图表、讲者备注、独立 critic | 输出可编辑、备注与交付前独立检查 |
| [likaku/Mck-ppt-design-skill](https://github.com/likaku/Mck-ppt-design-skill) | 267 | 咨询式布局系统、70 种 pattern、机器 gate | 分阶段 harness、门禁结果由脚本派生、规则集中化 |

这些 star 数据来自 GitHub API 快照。它们不能直接比较：HTML slide 与 PPTX skill 的受众、发布时间和传播渠道不同。

### 许可边界

- Guizang 为 AGPL-3.0。
- Mck 为 Apache-2.0。
- Academic-pptx-skill、slides_maker、frontend-slides 为 MIT（快照时）。
- Anthropic PPTX skill 有其独立许可。

本项目只借鉴公开描述与设计思想，脚本为重新实现，不复制受限代码或资产。

## 4. Meta-skill / Harness 借鉴

### 渐进披露

问题：把所有设计规则塞进一个超长 SKILL.md，会占用上下文，也让 agent 忽略重点。

决策：

- 入口只给阶段路由。
- 图表任务才读 data-storytelling。
- 流程任务才读 diagram-patterns。
- QA 阶段才读 qa-checklist。

### 机读门禁

问题：Agent 容易“脑内检查完毕”，然后宣布通过。

决策：

- `lint_deck.py` 决定 spec 门禁。
- `inspect_pptx.py` 决定结构门禁。
- `render_preview.py` 生成可看证据。
- `smoke_test.py` 将全链路返回码汇总。
- 对话中的解释不能覆盖脚本的 FAIL/ERROR。

### 配置与代码分离

问题：颜色、坐标与规则散落在代码中，新增主题或版式会产生分叉。

决策：

- Theme/typography：`design-tokens.yaml`。
- Canvas/bleed/type mapping：`layout-registry.yaml`。
- 内容：`spec.yaml`。
- 逻辑：`scripts/*.py`。

## 5. Storytelling with Data

来源：

- https://www.storytellingwithdata.com/
- https://www.storytellingwithdata.com/blog/2022/2/1/swdchallenge-declutter-and-focus
- https://www.storytellingwithdata.com/letspractice/downloads

核心过程：

1. 理解语境。
2. 选择合适视觉。
3. 消除杂乱。
4. 聚焦注意力。
5. 像设计师一样思考。
6. 讲故事。

落地：

- `deck.audience` 与 `desired_action` 强制存在。
- 图表类型受控。
- 去网格、去图例框、直接标注。
- 其他数据灰色、最多两项高亮。
- 每图 source 必填。
- action title 先说结论。
- 图表连续不超过两页。

## 6. Duarte sparkline 与情绪对比

来源：

- https://www.duarte.com/blog/ultimate-guide-to-contrast/
- https://www.duarte.com/blog/business-communication-demands-3-act-story-structure/

借鉴：

- 在“现状”和“可能”之间制造对比。
- 通过峰谷而不是单调升级维持注意力。
- 结尾落在“新常态”与行动，而不是总结目录。

本实现将抽象对比转换为每页 `energy` 与 `mood`，并通过 lint 检查开场、低谷、结尾峰值和变化幅度。

## 7. Bleed 设计依据

来源：

- https://stephanieevergreen.com/bleed-your-presentation/

借鉴：

- 图像触及边缘可取消“相框感”，提高沉浸感。
- Bleed 应服务重点，不是每页默认。

本实现扩展为 full、overlay、partial、half、edge 与 color-block，并设定 40% 的强 bleed 预算、scrim、分辨率与叠字上限。

## 8. 为什么选择当前技术栈

### python-pptx

优点：

- Python 生态易于和 YAML、Pillow、Matplotlib 组合。
- 形状、文字、备注与图片可生成原生 PPTX。
- 便于独立开发者阅读和修改。

限制：

- 高级动画与某些原生图表控制有限。
- 字体与文本溢出必须靠渲染 QA。
- OOXML 透明度需谨慎处理。

### Matplotlib 图表 PNG

优点：稳定、可控、符合 SWD 的去杂乱与直接标注。

限制：PowerPoint 中不可直接编辑数据。未来可添加 native chart backend，但不能牺牲聚焦和来源规则。

### Pillow

用于 cover crop、焦点裁切和 gradient scrim，避免图片拉伸与依赖 PowerPoint 渐变差异。

## 9. 本轮审计修复

从原始未完成材料继续时，完成了这些关键修复：

- 修复 flow badge 调用中先解包空 rect 导致的运行时异常。
- 将流程图重写为有名称、可检查、节点不足时明确失败的实现。
- 增加 `big_idea / audience / desired_action` lint。
- 流程图从“允许无高亮”改为“恰好一个高亮”。
- 增加图表 series 数量、name 与数值类型检查。
- 修复 Matplotlib CJK 字体优先级。
- Scrim 图片从低分辨率检查中排除。
- 修复 partial-left 浅色图片上的页脚对比问题。
- 补齐可运行示例素材，并完成 lint/build/render/inspect 全链路。

## 10. 1.0 基线未纳入的能力

- 修改既有 PPTX 模板。
- PowerPoint 原生可编辑 chart backend。
- 动画与渐进点击构建。
- 自动生成真实产品照片。
- 复杂网络图、Sankey、地图与 3D。
- 自动校验所有像素级对比度。

这些能力可以扩展，但不应让窄域工作流变成一个无法维护的通用 PPT 引擎。1.1 已在不承担任意 PPTX 逆向编辑的前提下，加入 source-backed iteration、可编辑 UI mockup、版本 lineage、主题预算与新 bleed/type；原生 chart、动画和模板保真仍不在范围内。
