# Changelog

## 1.2.0 — 2026-09-03

- Cards 流程支持每步一个下置象形图，用卡片下半部增强扫读，不与 desc 并存。
- 新增图标全覆盖、结构限制与资产存在性 lint；缺图、部分配图或非 horizontal/cards 使用会失败。
- SVG 作为可维护源文件，PPTX 嵌入透明 PNG 兼容渲染，降低 PowerPoint/LibreOffice 渲染差异。
- 单元测试与流程图审美规范同步升级。
- Manifest 的 `source_spec` 改为相对路径，避免公开产物泄露本机用户名与绝对目录。

## 1.1.0 — 2026-09-03

- 支持具备 spec、脚本与 manifest 的 source project 多轮迭代，新增 lineage、父 manifest 哈希与回归页规则。
- 新增原生 PowerPoint 形状组成的可编辑 UI mockup 公共 renderer。
- Inspect 新增 UI shell、标题栏、divider、主题 effect 与重复实例一致性 QA。
- 新增 `topic_budgets` / `slides[].topics` 篇幅预算门禁。
- 新增 `half-top`、`half-bottom` 上下半屏 bleed。
- 新增 `media_bars` 条目与专属配图一一对应版式，默认文字 bar 占 60% 且可配置。
- 示例、单元测试、smoke test、references 与 UI metadata 同步升级。

## 1.0.0 — 2026-09-02

- 完成 Agent Skills 标准入口、Codex metadata 与知识路由。
- 建立 Big Idea、三幕、energy/mood 和 bleed 预算工作流。
- 提供 ink、paper、signal 三套主题与 13 种页面 type。
- 提供 full、overlay、partial、half、edge、color-block 等 8 种 bleed 模式。
- 提供 SWD 风格 bar/hbar/line/slope/dot 图表。
- 提供 cards/chevron/vertical/layers 原生流程图。
- 增加 spec lint、PPTX inspect、LibreOffice/Poppler 视觉预览。
- 修复原始 flow badge 空 rect 异常、CJK 图表字体与 partial-left 页脚对比问题。
- 提供 12 页可运行示例、单元测试与 smoke test。
