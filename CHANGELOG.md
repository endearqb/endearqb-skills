## Changelog

### endearqb-community-profiler

-   **Added**: 新增社区成员画像分析技能，支持从群聊记录中识别核心贡献者、潜水者、活跃用户和 KOL，生成五维画像评分并输出可视化报告。

### endearqb-svg-flowchart

-   **Added**: 新增 SVG 流程图生成技能，支持将文字步骤转换为标准 SVG 文件，覆盖垂直/水平布局、判断分支、多列分组流程图，并可选生成 HTML 预览页；附带 `svg-spec.md` 统一规范箭头、节点尺寸、坐标公式和主题配色。

### endearqb-wechat-file-organizer

-   **Added**: 新增 Windows 微信文件整理技能，支持自动检测微信文件目录、统一 dry-run 预览、识别括号序号重复文件并移入回收站、按月份和类型分类复制文件，以及按最近 N 个月时间范围过滤整理。
-   **Updated**: 哈希值命名的视频和图片通过文件大小判断重复。

### endearqb-lab-report-writer

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| 2.4.0 | 2026-04-12 | **三项优化**：① `ask_user_question` 新增第五个问题「HTML 内联编辑功能」，默认不启用，用户选择后 `build_html.py` 传 `--editable`，`report.js` 改为按 `data-editable="true"` 属性条件初始化编辑器；② 数据验证跳过时 `build_html.py` 传 `--no-verify-panel`，HTML 中不渲染验证面板 `<aside>`；③ 移动端目录悬浮按钮从左下角（`left:24px`）移至右下角（`right:24px`），菜单弹层同步改为 `right:16px` |
| 2.3.2 | 2026-04-06 | **可视化规范补充两条经验**：① `第五步→SVG流程图规范` 新增「SVG `<text>` 内禁止嵌套 HTML 标签」规则，列出粗体/下标/斜体的正确 SVG 替代写法；② `第五步→数据可视化原则` 新增第7条「多系列量级差异大时优先分面图（Facet），避免双 Y 轴」规范，含必须使用双 Y 轴时的颜色区分要求 |
| 2.3.1 | 2026-04-05 | **橄榄学报配色修正**：meta-card / toc / 偶数行的色相从 H≈48°（黄调，与暖墨纸重叠）推向 H≈100°（黄绿调，与 accent #4a6741 对齐）；meta-card 渐变改为 `#dae7d4→#d0dec9`，toc 改为 `#ebf1e8`，偶数行改为 `#e6ece3`，边框跟随改为 `#b8cdb2`；SVG node-bg / node-alt 同步对齐 |
| 2.3.0 | 2026-04-05 | **SVG主题联动 + 页面色彩修复** |
| 2.2.2 | 2026-04-05 | **主题覆盖全面修复**：系统检查并补全所有6套主题的CSS覆盖范围，修复表格表头（`th`）、偶数行（`tbody tr:nth-child(even)`）、`td` 边框、摘要（`.abstract`）、目录（`.toc`）、引用块（`blockquote`）、公式块（`.formula`）、验证框（`.verification`）、图表容器（`.chart-container`）、元数据卡片（`.meta-card`）、验证面板（`.verify-panel-header`/`.verify-section-label`）、链接颜色（`a`）等元素在各主题下均有正确的颜色覆盖，消除跨主题视觉不一致问题 |
| 2.2.1 | 2026-04-05 | **SVG高度公式修正**：垂直流程图由旧公式 `N×80+20`（漏底部留白）改为 `N×80−4`（即 20+N×56+(N-1)×24+20，顶底各20px对称），消除末节点 stroke 被裁切问题；步骤数适配表改为公式驱动，4步模板 viewBox 高度从 380 修正为 316 |
| 2.2.0 | 2026-04-05 | **SVG模板精修**：三处统一改进——① 文字定位改用 `dominant-baseline="central"`（y 设为节点垂直中心），消除字体/平台偏移；② 箭头 marker 从 `refX="8" refY="3"` 改为 `refX="9" refY="3.5"`（配合 markerHeight=7），贴合节点边缘更精准；③ 所有矩形圆角统一为 `rx="8"`，与 svg-flowchart-maker skill 风格对齐 |
| 2.1.0 | 2026-03-30 | **SVG箭头方向规范**：`svg-flowchart-template.md` 新增「`orient="auto"` 核心机制」章节，明确箭头尖须指向 marker 本地 +x 方向（path 中 x 最大顶点为尖端），附常见错误排查表；SKILL.md 参考索引同步更新 |
| 2.0.0 | 2026-03-28 | **主题逻辑移入脚本**：6套预置主题 CSS 内置到 `build_html.py`，Agent 只需传 `--theme` 参数，无需读取 `style-constitution.md` 或内联任何 CSS，彻底消除主题相关 token 消耗；修正选项名「极夜深色→午夜藏青」「靛蓝理工→石墨极简」与脚本一致 |
| 1.9.0 | 2026-03-28 | **色彩主题选择**：`ask_user_question` 新增第四个问题，提供6套预置风格；`THEME` 工作变量驱动后续生成步骤 |
| 1.8.0 | 2026-03-26 | **生成前确认步骤**：信息采集完成后强制调用 `ask_user_question` 工具，同时确认文档模式（长/单文件）、可视化内容（SVG/Chart）、附加输出（Markdown），结果驱动后续所有生成步骤 |
| 1.7.0 | 2026-03-26 | **SVG 独立文件注入**：SVG 不再内嵌正文片段，改为独立 `.svg` 文件；`build_html.py` 新增 SVG 注入逻辑（扫描 `data-svg-src` 占位符）和 `--svg-dir` 参数；SKILL.md 新增占位符写法说明和架构图更新 |
| 1.6.0 | 2026-03-26 | **分段生成支持**：阶段一新增长报告分段策略（`body-parts/body-NN-*.html`）；`build_html.py` 新增 `--body-dir` 和 `--body-parts` 参数，按文件名升序自动合并；检查清单同步更新 |
| 1.5.0 | 2026-03-24 | **架构重构**：统一单一生成流程（report-body.html + charts-init.js + verify-output.txt → build\_html.py），CSS/JS 提取为 `assets/report.css` 和 `assets/report.js`，彻底消除正则解析脆弱性；`build_html.py` 重写为纯拼接器（149行）；删除"短报告直接生成"模式 |
| 1.4.0 | 2026-03-24 | 新增分段整合模式（已被1.5.0取代） |
| 1.3.1 | 2026-03-22 | 修复手机端图表高度塌陷 |
| 1.3.0 | 2026-03-20 | 移动端全面适配：4级断点、浮动导航按钮、表格触摸横滚 |
| 1.2.0 | 2026-03-20 | 数据验证移出正文，升级为悬浮面板三区展示 |
| 1.1.0 | 2026-03-20 | 修复目录双份序号 |
| 1.0.0 | — | 初始版本 |
