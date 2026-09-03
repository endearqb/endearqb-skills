# Skill evals

`evals.json` 给出用于评估本 skill 的代表性提示词和可观察通过条件。它不绑定某个评测框架；可由人工、Codex/Claude 子代理或外部 evaluator 执行。

每个 case 重点检查：

- 是否先形成 Big Idea、audience、desired action。
- 是否给出有峰谷的 energy 曲线。
- 是否在需要时读取相应 reference，而非全量加载。
- 是否生成 spec 并运行真实门禁。
- 是否渲染并看 contact sheet。
- 是否诚实标记示例数据和占位图。

正式评测时建议保存：prompt、生成目录、lint JSON、inspect JSON、contact sheet、grader 结论与耗时。
