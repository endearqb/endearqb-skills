# Reference index

> Skill 路径：`product-story-pptx/references/INDEX.md`

本目录承载不会在每次任务中都需要加载的设计知识。`SKILL.md` 只保留流程、硬规则与路由；当前阶段用到什么，才读什么。

## 文件职责

| 文件 | 何时读取 | 回答的问题 |
|---|---|---|
| `narrative-arc.md` | brief 完成后、逐页大纲前 | 故事如何起伏？每页应该让观众感到什么？ |
| `bleed-layouts.md` | 有照片、截图、hero、章节页时 | 图片如何出血、裁切、加 scrim，并形成节奏？ |
| `layout-system.md` | 为每页选择 type、文字量与网格时 | 该页用哪一种结构？如何避免重复与拥挤？ |
| `diagram-patterns.md` | 出现流程、架构、路线或系统关系时 | 应选什么拓扑？节点、箭头、高亮怎么做才克制？ |
| `data-storytelling.md` | 出现图表、KPI、对照、big number 时 | 图表如何先说结论，再聚焦数据？ |
| `visual-language.md` | 选择主题、字体、颜色、图片风格时 | 整份 deck 如何形成统一气质而不是模板拼盘？ |
| `qa-checklist.md` | 生成后 | lint、结构检查和肉眼检查分别看什么？ |
| `iteration-lineage.md` | 从已有 source project 继续多轮修改时 | 如何继承上版、记录谱系并确定回归范围？ |
| `editable-ui-mockups.md` | 用原生形状制作产品界面示意时 | 公共组件字段、几何不变量与重复实例 QA 是什么？ |
| `research-basis.md` | 维护、扩展或审计本 skill 时 | 设计规则来自哪些官方规范和社区实践？ |

## 实现文件映射

| 设计知识 | 可执行实现 |
|---|---|
| energy 与 bleed 预算 | `scripts/lint_deck.py` + `assets/layout-registry.yaml` |
| 页面坐标与 type↔bleed | `assets/layout-registry.yaml` |
| 字体、字号、主题与图表色 | `assets/design-tokens.yaml` |
| 图表 | `scripts/chart_swd.py` |
| 流程图 | `scripts/flow_diagram.py` |
| 可编辑 UI mockup | `scripts/ui_mockup.py` |
| PPTX 生成 | `scripts/build_deck.py` |
| 渲染预览 | `scripts/render_preview.py` / `scripts/thumbnail.py` |
| 结构 QA | `scripts/inspect_pptx.py` |
| 全链路回归 | `scripts/smoke_test.py` |

## 扩展纪律

新增规则时按以下优先级落位：

1. 能机器判断的，写入 `lint_deck.py` 或 `inspect_pptx.py`。
2. 影响所有主题的尺寸与坐标，写入 YAML tokens/registry。
3. 需要人类判断的审美原则，写入对应 reference。
4. 新增页面能力，同时更新 spec 注释、registry、builder、lint、示例与 smoke test。
5. 不要只修改某一个文件，导致“文档说能用、脚本却不支持”。
