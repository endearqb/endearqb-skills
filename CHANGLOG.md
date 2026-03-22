## Changelog

### endearqb-community-profiler

- **Added**: 新增社区成员画像分析技能，支持从群聊记录中识别核心贡献者、潜水者、活跃用户和 KOL，生成五维画像评分并输出可视化报告。

### endearqb-lab-report-writer

<table style="min-width: 75px;"><colgroup><col style="min-width: 25px;"><col style="min-width: 25px;"><col style="min-width: 25px;"></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>版本</p></th><th colspan="1" rowspan="1"><p>日期</p></th><th colspan="1" rowspan="1"><p>变更</p></th></tr><tr><td colspan="1" rowspan="1"><p>1.3.1</p></td><td colspan="1" rowspan="1"><p>2026-03-22</p></td><td colspan="1" rowspan="1"><p>修复手机端图表高度塌陷：<code>.chart-container canvas</code> 加 <code>min-height: 200px</code>（桌面）/ <code>220px</code>（≤768px）；移动端 JS 检测自动将所有图表 <code>maintainAspectRatio</code> 设为 <code>false</code>，高度由 CSS 控制，不再跟随宽度联动缩放</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.3.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>移动端全面适配：4 级断点(1024/768/480/360px)、移动端浮动导航按钮(☰)、表格触摸横滚、字号阶梯缩放、深色模式适配、横屏优化、编辑器按钮移动端始终可见、验证面板移动端底部全宽</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.2.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>数据验证移出正文：HTML无验证章节，Markdown文末加附录；验证面板升级为三区详细展示（统计摘要/计算验证/偏差汇总），面板宽度 360→460px</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.1.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>修复目录双份序号：<code>html-template.md</code> 中 <code>.toc ol</code> 改为 <code>padding-left: 0; list-style: none</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>1.0.0</p></td><td colspan="1" rowspan="1"><p>—</p></td><td colspan="1" rowspan="1"><p>初始版本</p></td></tr></tbody></table>
