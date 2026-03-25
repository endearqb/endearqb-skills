## Changelog

### endearqb-community-profiler

-   **Added**: 新增社区成员画像分析技能，支持从群聊记录中识别核心贡献者、潜水者、活跃用户和 KOL，生成五维画像评分并输出可视化报告。
    

### endearqb-lab-report-writer

<table style="min-width: 75px;"><colgroup><col style="min-width: 25px;"><col style="min-width: 25px;"><col style="min-width: 25px;"></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>版本</p></th><th colspan="1" rowspan="1"><p>日期</p></th><th colspan="1" rowspan="1"><p>变更</p></th></tr><tr><td colspan="1" rowspan="1"><p>1.5.0</p></td><td colspan="1" rowspan="1"><p>2026-03-24</p></td><td colspan="1" rowspan="1"><p><strong>架构重构</strong>：统一单一生成流程（report-body.html + charts-init.js + verify-output.txt → build_html.py），CSS/JS 提取为 <code>assets/report.css</code> 和 <code>assets/report.js</code>，彻底消除正则解析脆弱性；<code>build_html.py</code> 重写为纯拼接器（149行）；删除"短报告直接生成"模式</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.4.0</p></td><td colspan="1" rowspan="1"><p>2026-03-24</p></td><td colspan="1" rowspan="1"><p>新增分段整合模式（已被1.5.0取代）</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.3.1</p></td><td colspan="1" rowspan="1"><p>2026-03-22</p></td><td colspan="1" rowspan="1"><p>修复手机端图表高度塌陷</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.3.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>移动端全面适配：4级断点、浮动导航按钮、表格触摸横滚</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.2.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>数据验证移出正文，升级为悬浮面板三区展示</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.1.0</p></td><td colspan="1" rowspan="1"><p>2026-03-20</p></td><td colspan="1" rowspan="1"><p>修复目录双份序号</p></td></tr><tr><td colspan="1" rowspan="1"><p>1.0.0</p></td><td colspan="1" rowspan="1"><p>—</p></td><td colspan="1" rowspan="1"><p>初始版本</p></td></tr></tbody></table>