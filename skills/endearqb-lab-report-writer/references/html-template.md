# HTML报告模板参考

本文件包含生成期刊风格HTML实验报告所需的完整骨架和CSS。每次生成HTML时必须参照此文件的配色、字体、排版规范。

---

## 完整HTML骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#2f4f4f">
<title>[报告标题]</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
/* ===== CSS变量（配色系统，严格遵守） ===== */
:root {
  --paper: #fbfaf6;
  --page:  #ffffff;
  --ink:   #1f2328;
  --muted: #5c6570;
  --line:  #d7d0c3;
  --soft:  #f5f1e7;
  --soft-alt: #eef4f1;
  --soft-blue: #f3f6fb;
  --accent: #2f4f4f;
  --shadow: 0 18px 48px rgba(31,35,40,0.10);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }

body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(47,79,79,0.08), transparent 30%),
    linear-gradient(180deg, #f6f4ee 0%, var(--paper) 100%);
  color: var(--ink);
  font-family: Georgia, "Noto Serif SC", "Songti SC", "STSong", serif;
  line-height: 1.82;
}

/* ===== 页面容器 ===== */
.page {
  max-width: 980px;
  margin: 28px auto 48px;
  padding: 46px 52px 60px;
  background: var(--page);
  box-shadow: var(--shadow);
  border: 1px solid rgba(31,35,40,0.06);
}

/* ===== 期刊顶栏 ===== */
.journal-bar {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  font: 600 12px/1.4 "Helvetica Neue", Arial, sans-serif;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  border-top: 3px solid var(--ink);
  border-bottom: 1px solid var(--line);
  padding: 12px 0;
  margin-bottom: 30px;
}

/* ===== 封面区 ===== */
.cover {
  display: grid;
  grid-template-columns: 1.65fr 0.95fr;
  gap: 22px;
  align-items: start;
}

h1 {
  margin: 0 0 12px;
  font-size: 35px;
  line-height: 1.25;
  letter-spacing: -0.02em;
}

.subtitle {
  margin: 0 0 14px;
  color: #46505a;
  font-size: 17px;
}

/* ===== 元数据卡片（右侧）===== */
.meta-card {
  background: linear-gradient(180deg, #f8f6ef 0%, #f3efe5 100%);
  border: 1px solid var(--line);
  padding: 18px 18px 16px;
}

.meta-card h2,
.toc h2,
.references h2 {
  margin: 0 0 10px;
  font-size: 14px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.meta-card dl {
  margin: 0;
  display: grid;
  grid-template-columns: 84px 1fr;
  gap: 8px 12px;
  font-size: 14px;
}

.meta-card dt { color: var(--muted); font-family: "Helvetica Neue", Arial, sans-serif; }

/* ===== 摘要 ===== */
.abstract {
  margin: 28px 0 20px;
  padding: 22px 24px 20px;
  background: #f6f4ed;
  border-left: 4px solid var(--ink);
}

.abstract h2 {
  margin: 0 0 10px;
  font-size: 13px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink);
}

.abstract p { margin: 0; font-size: 15px; }
.keywords { margin-top: 12px; color: #47515b; font-family: "Helvetica Neue", Arial, sans-serif; }

/* ===== 目录 ===== */
.toc {
  margin: 24px 0 8px;
  padding: 16px 18px;
  border: 1px solid var(--line);
  background: #fbfaf6;
}
.toc ol { margin: 0; padding-left: 0; list-style: none; }
.toc li { margin: 8px 0; }

/* ===== 分割线 ===== */
.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--line), transparent);
  margin: 32px 0 20px;
}

/* ===== 标题系统 ===== */
h2.section-title {
  margin: 34px 0 16px;
  font-size: 24px;
  line-height: 1.35;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--line);
}

h3 { margin: 28px 0 10px; font-size: 19px; }
h4 { margin: 20px 0 8px; font-size: 16px; }
p  { margin: 0 0 14px; text-align: justify; }
ul, ol { margin: 0 0 16px 22px; padding: 0; }
li { margin: 7px 0; }

/* ===== 公式块 ===== */
.formula {
  margin: 16px 0 18px;
  padding: 14px 16px;
  background: var(--soft-blue);
  border: 1px solid #d9dfea;
  font-family: "Courier New", monospace;
  white-space: pre-wrap;
  font-size: 14px;
}

/* ===== 提示框/说明框 ===== */
.callout {
  margin: 18px 0;
  padding: 14px 16px;
  background: linear-gradient(180deg, #edf4f1 0%, #f7fbfa 100%);
  border-left: 4px solid #3f6b68;
}

/* ===== 验证结果框 ===== */
.verification {
  margin: 18px 0;
  padding: 14px 16px;
  background: #f8fdf8;
  border: 1px solid #c8e6c9;
  border-left: 4px solid #4caf50;
  font-family: "Courier New", monospace;
  font-size: 13px;
}

.verification .warn {
  color: #e65100;
  border-left-color: #ff9800;
}

/* ===== 悬浮验证面板（右下角，默认折叠）===== */
/* 备用：若用户要求附录式，直接用 .verification 块，删除此面板 */

.verify-panel {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 460px;
  max-width: calc(100vw - 48px);
  background: var(--page);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(31,35,40,0.14);
  z-index: 8000;
  font-family: "Helvetica Neue", Arial, sans-serif;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

/* 有偏差时面板边框变橙警示 */
.verify-panel.has-warn {
  border-color: #f59e0b;
  box-shadow: 0 8px 32px rgba(245,158,11,0.18);
}

/* 标题栏（点击区域）*/
.verify-panel-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: var(--soft);
  border: none;
  cursor: pointer;
  font: 600 13px/1.4 "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  text-align: left;
  transition: background 0.15s;
}
.verify-panel-header:hover { background: var(--soft-alt); }

.verify-panel-icon { font-size: 15px; flex-shrink: 0; }

.verify-panel-title { flex: 1; letter-spacing: 0.04em; }

/* 通过数/偏差数 小徽章 */
.verify-panel-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
  background: #dcfce7;
  color: #166534;
  white-space: nowrap;
}
.verify-panel.has-warn .verify-panel-badge {
  background: #fef3c7;
  color: #92400e;
}

/* 折叠箭头 */
.verify-panel-chevron {
  font-size: 10px;
  color: var(--muted);
  transition: transform 0.2s ease;
  flex-shrink: 0;
}
.verify-panel.open .verify-panel-chevron { transform: rotate(180deg); }

/* 面板主体（折叠时 height:0，展开时 auto）*/
.verify-panel-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}
.verify-panel.open .verify-panel-body {
  max-height: 420px;
  overflow-y: auto;
}

/* 验证内容等宽字体块 */
.verify-pre {
  margin: 0;
  padding: 14px 16px;
  font: 12px/1.65 "Courier New", Consolas, monospace;
  color: var(--ink);
  white-space: pre-wrap;
  word-break: break-all;
  background: transparent;
  border: none;
  border-top: 1px solid var(--line);
}

/* 偏差说明建议文字（可选）*/
.verify-note {
  margin: 0;
  padding: 8px 16px 12px;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
  border-top: 1px solid var(--line);
  display: none;
}
.verify-note:not(:empty) { display: block; }

/* 验证面板内分区 */
.verify-section {
  border-top: 1px solid var(--line);
}
.verify-section-label {
  padding: 6px 14px 4px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--muted);
  text-transform: uppercase;
  background: var(--soft);
}
.verify-warn-section .verify-section-label {
  color: #92400e;
  background: #fef3c7;
}

/* 打印时隐藏 */
@media print { .verify-panel { display: none !important; } }

/* 移动端贴底全宽 */
@media (max-width: 768px) {
  .verify-panel {
    bottom: 0;
    right: 0;
    left: 0;
    width: 100%;
    max-width: 100%;
    border-radius: 12px 12px 0 0;
  }
  .verify-panel.open .verify-panel-body {
    max-height: 55vh;
  }
}

/* ===== 表格 ===== */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0 22px;
  font-size: 14px;
}

th {
  background: var(--ink);
  color: #fff;
  text-align: left;
  padding: 10px 12px;
  font: 600 13px/1.45 "Helvetica Neue", Arial, sans-serif;
}

td {
  padding: 10px 12px;
  border-bottom: 1px solid #ece7dd;
  vertical-align: top;
}

tbody tr:nth-child(even) td { background: #faf8f2; }

/* ===== 图表区域 ===== */
figure { margin: 22px 0 24px; }

figcaption {
  margin-top: 10px;
  text-align: center;
  color: var(--muted);
  font-style: italic;
  font-size: 13px;
}

.chart-container {
  position: relative;
  margin: 16px 0;
  padding: 16px;
  background: #fafaf8;
  border: 1px solid var(--line);
}

/* ===== 参考文献 ===== */
.references {
  margin-top: 38px;
  padding-top: 18px;
  border-top: 2px solid var(--ink);
}

.references ol { margin-left: 20px; font-size: 14px; }
.references li { margin-bottom: 10px; word-break: break-word; }

/* ===== 页脚 ===== */
.footer {
  margin-top: 32px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font: 12px/1.5 "Helvetica Neue", Arial, sans-serif;
  color: var(--muted);
}

/* ===== 悬浮目录（宽屏侧边，不侵入正文）===== */

/* 布局容器：把 .page 和 .float-toc 并排放，只在足够宽时生效 */
.report-layout {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 0;
}

/* 悬浮目录本体 */
.float-toc {
  display: none; /* 默认隐藏，由媒体查询开启 */
  position: sticky;
  top: 32px;
  width: 200px;
  flex-shrink: 0;
  margin-left: 24px;
  padding: 16px 16px 14px;
  background: var(--page);
  border: 1px solid var(--line);
  box-shadow: 0 4px 18px rgba(31,35,40,0.07);
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 12.5px;
  line-height: 1.5;
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--line) transparent;
}

.float-toc-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--line);
}

.float-toc ol {
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: none;
}

.float-toc li {
  margin: 0;
}

.float-toc a {
  display: block;
  padding: 5px 8px;
  color: var(--muted);
  text-decoration: none;
  border-left: 2px solid transparent;
  border-radius: 0 3px 3px 0;
  transition: color 0.18s, border-color 0.18s, background 0.18s;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.float-toc a:hover {
  color: var(--ink);
  background: var(--soft);
}

/* 当前阅读位置高亮 */
.float-toc a.active {
  color: var(--accent);
  border-left-color: var(--accent);
  background: var(--soft-alt);
  font-weight: 600;
}

/* 子节缩进（h3级别） */
.float-toc .sub {
  padding-left: 20px;
  font-size: 11.5px;
}

/* ===== 移动端浮动导航按钮（1024px 以下替代侧边目录）===== */
.mobile-nav-btn {
  display: none; /* 默认隐藏，由媒体查询开启 */
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 18px;
  border: none;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(47,79,79,0.40);
  z-index: 8100;
  transition: transform 0.2s ease, background 0.2s ease;
  -webkit-tap-highlight-color: transparent;
}
.mobile-nav-btn:hover,
.mobile-nav-btn:active { transform: scale(1.08); background: #3d6b6b; }

/* 展开状态：图标变 × */
.mobile-nav-btn.open::after { content: '✕'; }
.mobile-nav-btn:not(.open)::after { content: '☰'; }

/* 目录菜单弹层 */
.mobile-nav-menu {
  display: none;
  position: fixed;
  bottom: 78px;
  left: 16px;
  width: min(280px, calc(100vw - 32px));
  background: var(--page);
  border: 1px solid var(--line);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(31,35,40,0.18);
  z-index: 8090;
  overflow: hidden;
  animation: mobileNavIn 0.22s cubic-bezier(0.34,1.56,0.64,1) forwards;
}
.mobile-nav-menu.open { display: block; }

@keyframes mobileNavIn {
  from { opacity: 0; transform: translateY(12px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.mobile-nav-label {
  padding: 10px 16px 8px;
  font: 700 11px/1 "Helvetica Neue", Arial, sans-serif;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  border-bottom: 1px solid var(--line);
}

.mobile-nav-menu ol {
  margin: 0;
  padding: 8px 0;
  list-style: none;
  max-height: 60vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.mobile-nav-menu li { margin: 0; }

.mobile-nav-menu a {
  display: block;
  padding: 11px 16px;
  font: 14px/1.4 "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  text-decoration: none;
  min-height: 44px;
  display: flex;
  align-items: center;
  border-left: 3px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}
.mobile-nav-menu a:active,
.mobile-nav-menu a:hover {
  background: var(--soft);
  border-left-color: var(--accent);
}
.mobile-nav-menu li.sub a {
  padding-left: 28px;
  font-size: 13px;
  color: var(--muted);
}

/* 遮罩层（点击空白处关闭菜单）*/
.mobile-nav-overlay {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 8080;
  background: rgba(0,0,0,0.25);
}
.mobile-nav-overlay.open { display: block; }

/* ===== 响应式 — 多断点完整实现 ===== */

/* 1280px+：宽屏，悬浮侧边目录显示 */
@media (min-width: 1280px) {
  .float-toc { display: block; }
}

/* 1024px 以下：平板及手机，隐藏侧边目录，改用移动端浮动导航按钮 */
@media (max-width: 1024px) {
  .float-toc { display: none !important; }
  .mobile-nav-btn { display: flex; }
}

/* 1024px 以下：布局收窄 */
@media (max-width: 1024px) {
  .page { margin: 0 auto; padding: 28px 28px 44px; max-width: 100%; }
}

/* 768px 以下：平板竖屏 / 大手机 */
@media (max-width: 768px) {
  .page { margin: 0; padding: 20px 18px 36px; box-shadow: none; border: none; border-radius: 0; }
  .cover { grid-template-columns: 1fr; gap: 16px; }
  .meta-card { margin-top: 4px; }
  .journal-bar { flex-direction: column; gap: 4px; font-size: 11px; padding: 10px 0; }
  .footer { flex-direction: column; gap: 4px; font-size: 11px; }
  h1 { font-size: 26px; }
  h2.section-title { font-size: 21px; }
  h3 { font-size: 17px; }
  /* 表格横向滚动 */
  .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 -18px; padding: 0 18px; }
  table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; white-space: nowrap; }
  th, td { white-space: nowrap; }
  /* 代码 / 公式块横滚 */
  .formula, pre { overflow-x: auto; -webkit-overflow-scrolling: touch; }
  svg { width: 100%; height: auto; }
  .chart-container { padding: 10px; }
  .abstract { padding: 16px 14px 14px; }
}

/* 480px 以下：大多数手机竖屏 */
@media (max-width: 480px) {
  .page { padding: 16px 14px 28px; }
  h1 { font-size: 22px; line-height: 1.3; }
  h2.section-title { font-size: 19px; }
  h3 { font-size: 16px; }
  h4 { font-size: 14.5px; }
  p, li { font-size: 14px; line-height: 1.75; }
  td { font-size: 13px; }
  .abstract p, .keywords { font-size: 13.5px; }
  .abstract { padding: 14px 12px 12px; }
  .meta-card dl { grid-template-columns: 68px 1fr; font-size: 13px; gap: 6px 10px; }
  .formula { font-size: 12.5px; padding: 10px 12px; }
  .verification { font-size: 12px; padding: 10px 12px; }
  table { font-size: 12.5px; }
  th, td { padding: 7px 9px; }
  .journal-bar { font-size: 10.5px; }
  .toc { padding: 12px 12px; }
  .toc li { margin: 6px 0; font-size: 13.5px; }
  .footer { font-size: 10.5px; }
  .callout { padding: 12px 13px; }
}

/* 360px 以下：超小屏（老款 Android / 小尺寸机型）*/
@media (max-width: 360px) {
  .page { padding: 12px 11px 24px; }
  h1 { font-size: 19px; }
  h2.section-title { font-size: 17px; }
  h3 { font-size: 15px; }
  p, li { font-size: 13.5px; }
  .meta-card dl { grid-template-columns: 60px 1fr; font-size: 12.5px; }
  .formula { font-size: 12px; }
  th, td { padding: 6px 7px; font-size: 12px; }
}

/* 横屏手机（高度 < 500px）：减少垂直留白 */
@media (max-height: 500px) and (orientation: landscape) {
  .page { padding-top: 12px; padding-bottom: 20px; }
  h1 { font-size: 20px; margin-bottom: 6px; }
  .abstract { margin: 14px 0 12px; }
  .verify-panel { bottom: 8px; right: 8px; }
  .mobile-nav-btn { bottom: 8px; left: 8px; }
}

/* 深色模式移动端适配 */
@media (prefers-color-scheme: dark) and (max-width: 768px) {
  :root {
    --paper: #1a1d23;
    --page:  #22262e;
    --ink:   #e8eaf0;
    --muted: #9ba3b2;
    --line:  #3a3f4d;
    --soft:  #2a2e38;
    --soft-alt: #252930;
    --soft-blue: #1e2535;
    --accent: #5f9ea0;
    --shadow: 0 18px 48px rgba(0,0,0,0.45);
  }
  body {
    background: var(--paper);
  }
  .meta-card {
    background: linear-gradient(180deg, #272b35 0%, #23272f 100%);
  }
  .abstract { background: #252930; }
  .toc { background: var(--paper); }
  tbody tr:nth-child(even) td { background: #282c36; }
  .chart-container { background: #1e2228; }
  th { background: #3a3f4d; }
}

@media print {
  body { background: #fff; }
  .page { box-shadow: none; margin: 0; max-width: none; border: none; padding: 0; }
  .float-toc, .mobile-nav-btn, .mobile-nav-menu { display: none !important; }
}
</style>
</head>
<body>

<!-- 布局容器：正文 + 右侧悬浮目录并排 -->
<div class="report-layout">
<main class="page">
  <!-- 正文内容（不变）-->

  <!-- 期刊顶栏 -->
  <div class="journal-bar">
    <div>[期刊/课程/机构名称]</div>
    <div>Report Date: [日期]</div>
  </div>

  <!-- 封面区 -->
  <section class="cover">
    <div>
      <h1>[实验报告标题]</h1>
      <p class="subtitle">[副标题或实验编号]</p>
    </div>
    <aside class="meta-card">
      <h2>Report Info</h2>
      <dl>
        <dt>作者</dt><dd>[姓名]</dd>
        <dt>学号/工号</dt><dd>[编号]</dd>
        <dt>指导教师</dt><dd>[教师名]</dd>
        <dt>实验日期</dt><dd>[日期]</dd>
        <dt>提交日期</dt><dd>[日期]</dd>
        <dt>课程</dt><dd>[课程名称]</dd>
      </dl>
    </aside>
  </section>

  <!-- 摘要 -->
  <section class="abstract">
    <h2>Abstract</h2>
    <p>[摘要内容，150-300字，包含：目的、方法、主要结果、结论]</p>
    <p class="keywords"><strong>关键词：</strong>[关键词1]；[关键词2]；[关键词3]</p>
  </section>

  <!-- 目录 -->
  <nav class="toc">
    <h2>Contents</h2>
    <ol>
      <li><a href="#intro">1. 引言</a></li>
      <li><a href="#theory">2. 实验原理</a></li>
      <li><a href="#methods">3. 实验装置与方法</a></li>
      <li><a href="#results">4. 实验结果</a></li>
      <li><a href="#analysis">5. 数据处理与分析</a></li>
      <li><a href="#discussion">6. 讨论</a></li>
      <li><a href="#conclusion">7. 结论</a></li>
      <li><a href="#references">参考文献</a></li>
    </ol>
  </nav>

  <div class="divider"></div>

  <!-- 正文各节 -->
  <section id="intro">
    <h2 class="section-title">1. 引言</h2>
    <p>[背景、研究意义、实验目的]</p>
  </section>

  <section id="theory">
    <h2 class="section-title">2. 实验原理</h2>
    <p>[理论基础]</p>
    <div class="formula">[公式，如：η = (m_实 - m_理) / m_理 × 100%]</div>
  </section>

  <section id="methods">
    <h2 class="section-title">3. 实验装置与方法</h2>
    <!-- SVG流程图插入位置 -->
    <figure>
      <svg><!-- 流程图 --></svg>
      <figcaption>图 1. 实验流程图</figcaption>
    </figure>
  </section>

  <section id="results">
    <h2 class="section-title">4. 实验结果</h2>
    <!-- 数据表格 -->
    <table>
      <thead><tr><th>参数</th><th>数值</th><th>单位</th></tr></thead>
      <tbody>
        <tr><td>[参数名]</td><td>[值]</td><td>[单位]</td></tr>
      </tbody>
    </table>
    <!-- Chart.js图表 -->
    <figure>
      <div class="chart-container">
        <canvas id="chart1"></canvas>
      </div>
      <figcaption>图 2. [描述性图题，说明核心发现]</figcaption>
    </figure>
  </section>

  <section id="analysis">
    <h2 class="section-title">5. 数据处理与分析</h2>

    <h3>5.1 计算过程</h3>
    <p>[推导步骤]</p>

    <h3>5.2 误差分析</h3>
    <p>[误差来源与量化]</p>
    <!-- 数据验证不在正文出现，完整详情见右下角悬浮验证面板（#verifyPanel）-->
  </section>

  <section id="discussion">
    <h2 class="section-title">6. 讨论</h2>
    <p>[对结果的解读、与预期的对比、可能的改进]</p>
  </section>

  <section id="conclusion">
    <h2 class="section-title">7. 结论</h2>
    <p>[简洁总结主要发现和意义]</p>
  </section>

  <section id="references" class="references">
    <h2>参考文献</h2>
    <ol>
      <li>[作者]. <em>[文献标题]</em>. [期刊/出版社], [年份].</li>
    </ol>
  </section>

  <footer class="footer">
    <span>[课程/机构名称] — 实验报告</span>
    <span>生成日期：[日期]</span>
  </footer>

</main>

<!-- 悬浮目录（宽屏时显示在正文右侧）-->
<!-- 注意：生成报告时，li 内容需与正文章节 id 和标题保持一致 -->
<nav class="float-toc" id="floatToc" aria-label="文章目录">
  <p class="float-toc-label">目录</p>
  <ol>
    <li><a href="#intro">1. 引言</a></li>
    <li><a href="#theory">2. 实验原理</a></li>
    <li><a href="#methods">3. 实验装置与方法</a></li>
    <li><a href="#results">4. 实验结果</a></li>
    <li><a href="#analysis">5. 数据处理与分析</a></li>
    <li class="sub"><a href="#analysis">5.1 计算过程</a></li>
    <li class="sub"><a href="#analysis">5.2 误差分析</a></li>
    <li><a href="#discussion">6. 讨论</a></li>
    <li><a href="#conclusion">7. 结论</a></li>
    <li><a href="#references">参考文献</a></li>
  </ol>
</nav>

</div><!-- /.report-layout -->

<!-- 移动端浮动导航按钮（1024px 以下替代侧边目录）-->
<div class="mobile-nav-overlay" id="mobileNavOverlay"></div>
<nav class="mobile-nav-menu" id="mobileNavMenu" aria-label="快速导航">
  <div class="mobile-nav-label">目录</div>
  <ol>
    <li><a href="#intro">1. 引言</a></li>
    <li><a href="#theory">2. 实验原理</a></li>
    <li><a href="#methods">3. 实验装置与方法</a></li>
    <li><a href="#results">4. 实验结果</a></li>
    <li><a href="#analysis">5. 数据处理与分析</a></li>
    <li class="sub"><a href="#analysis">5.1 计算过程</a></li>
    <li class="sub"><a href="#analysis">5.2 误差分析</a></li>
    <li><a href="#discussion">6. 讨论</a></li>
    <li><a href="#conclusion">7. 结论</a></li>
    <li><a href="#references">参考文献</a></li>
  </ol>
</nav>
<button class="mobile-nav-btn" id="mobileNavBtn" aria-label="打开目录" aria-expanded="false"></button>

<!-- ===========================================
     悬浮验证面板
     位置：右下角，默认折叠，点击标题栏展开/收起
     有偏差项时标题栏自动变为警告色
     面板内分三区：统计摘要 / 计算验证 / 偏差汇总
     =========================================== -->
<aside id="verifyPanel" class="verify-panel" aria-label="数据验证摘要">
  <button class="verify-panel-header" id="verifyToggle" aria-expanded="false">
    <span class="verify-panel-icon">🔬</span>
    <span class="verify-panel-title">验证摘要</span>
    <span class="verify-panel-badge" id="verifyBadge"></span>
    <span class="verify-panel-chevron">▲</span>
  </button>
  <div class="verify-panel-body" id="verifyBody">

    <!-- 区域一：统计摘要 -->
    <div class="verify-section" id="verifyStats">
      <div class="verify-section-label">📊 统计摘要</div>
      <pre class="verify-pre" id="verifyStatsContent">
<!-- 从 auto_verify.py 输出中提取【统计摘要】块粘贴至此 -->
[暂无统计数据]
      </pre>
    </div>

    <!-- 区域二：计算验证 -->
    <div class="verify-section" id="verifyCalc">
      <div class="verify-section-label">🧮 计算验证</div>
      <pre class="verify-pre" id="verifyCalcContent">
<!-- 从 auto_verify.py 输出中提取【计算验证】块粘贴至此，含公式、计算值、偏差 -->
[暂无计算验证数据]
      </pre>
    </div>

    <!-- 区域三：偏差汇总（有 ✗ 时自动显示） -->
    <div class="verify-section verify-warn-section" id="verifyWarnSection" style="display:none">
      <div class="verify-section-label">⚠ 偏差汇总</div>
      <pre class="verify-pre" id="verifyWarnContent"></pre>
      <p class="verify-note" id="verifyNote"></p>
    </div>

  </div>
</aside>

<script>
/* ===========================================
   CHART.JS 初始化 — SWD原则配置
   注意：每次生成报告时，根据实际数据填写labels和datasets
   =========================================== */
const ctx1 = document.getElementById('chart1');
if (ctx1) {
  new Chart(ctx1, {
    type: 'line',  // 根据数据类型选择：line/bar/scatter
    data: {
      labels: [/* x轴标签 */],
      datasets: [{
        label: '[系列名]',
        data: [/* 数据点 */],
        borderColor: '#2f4f4f',
        backgroundColor: 'rgba(47,79,79,0.08)',
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: false }
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Helvetica Neue' } }
        },
        y: {
          grid: { color: '#f0ece2', lineWidth: 1 },
          border: { display: false },
          ticks: { font: { family: 'Helvetica Neue' } }
        }
      }
    }
  });
}

/* ===========================================
   FLOAT TOC — 悬浮目录滚动高亮
   用 IntersectionObserver 监听各节进入视口，
   自动给对应目录项加 .active 类
   =========================================== */
(function () {
  const toc   = document.getElementById('floatToc');
  if (!toc) return;

  const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  // 收集正文 section id
  const ids      = links.map(a => a.getAttribute('href').slice(1));
  const sections = ids.map(id => document.getElementById(id)).filter(Boolean);

  // 去重（子节 .sub 可能指向同一 id）
  const uniqueSections = [...new Set(sections)];

  let activeId = null;

  const setActive = (id) => {
    if (id === activeId) return;
    activeId = id;
    links.forEach(a => {
      const match = a.getAttribute('href') === '#' + id;
      a.classList.toggle('active', match);
    });
    // 让高亮项在目录中保持可见（目录本身有滚动条时）
    const activeLink = toc.querySelector('a.active');
    if (activeLink) {
      activeLink.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  };

  // IntersectionObserver：section 进入视口上半部分时激活
  const observer = new IntersectionObserver((entries) => {
    // 找出所有当前可见的 section，取 y 坐标最小（最靠近顶部）的
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible.length > 0) {
      setActive(visible[0].target.id);
    }
  }, {
    rootMargin: '-10% 0px -60% 0px',  // 触发区：视口上方10%到中间40%
    threshold: 0
  });

  uniqueSections.forEach(sec => observer.observe(sec));

  // 平滑滚动（覆盖 CSS scroll-behavior，确保目录点击也有动画）
  links.forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();

/* ===========================================
   VERIFY PANEL — 悬浮验证面板控制器
   功能：
     · 点击标题栏或按 V 键展开/折叠
     · 自动扫描三区内容，统计 ✓ 和 ✗ 行，更新徽章
     · 有 ✗ 偏差项时：面板橙框、显示偏差汇总区、自动展开
     · 全部通过时：绿色徽章、默认折叠
   =========================================== */
(function () {
  const panel       = document.getElementById('verifyPanel');
  const toggle      = document.getElementById('verifyToggle');
  const body        = document.getElementById('verifyBody');
  const badge       = document.getElementById('verifyBadge');
  const statsEl     = document.getElementById('verifyStatsContent');
  const calcEl      = document.getElementById('verifyCalcContent');
  const warnSection = document.getElementById('verifyWarnSection');
  const warnContent = document.getElementById('verifyWarnContent');
  const note        = document.getElementById('verifyNote');
  if (!panel || !toggle) return;

  /* ---- 收集所有区域文本，统计通过/偏差数 ---- */
  function parseSummary() {
    const allText = [statsEl, calcEl].map(el => el ? el.textContent : '').join('\n');
    const passed  = (allText.match(/✓/g) || []).length;
    const warned  = (allText.match(/✗/g) || []).length;
    const total   = passed + warned;

    if (total === 0) {
      badge.textContent = '暂无数据';
      badge.style.background = '';
      return;
    }

    if (warned > 0) {
      panel.classList.add('has-warn');
      badge.textContent = `${passed}✓  ${warned}✗`;

      /* 提取偏差行，填充偏差汇总区 */
      if (warnSection && warnContent) {
        const warnLines = allText.split('\n')
          .filter(l => l.includes('✗'))
          .join('\n');
        warnContent.textContent = warnLines;
        warnSection.style.display = '';
      }

      if (note && !note.textContent.trim()) {
        note.textContent =
          `⚠ 发现 ${warned} 项计算偏差，报告正文保留原始数据，` +
          `建议在「讨论」节说明偏差原因。`;
      }
    } else {
      panel.classList.remove('has-warn');
      badge.textContent = `${passed}/${total} 通过`;
      if (warnSection) warnSection.style.display = 'none';
    }
  }

  /* ---- 展开/折叠 ---- */
  function open()  { panel.classList.add('open');    toggle.setAttribute('aria-expanded', 'true'); }
  function close() { panel.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
  function togglePanel() { panel.classList.contains('open') ? close() : open(); }

  /* ---- 有偏差时默认展开，全部通过则默认折叠 ---- */
  parseSummary();
  if (panel.classList.contains('has-warn')) open();

  toggle.addEventListener('click', togglePanel);

  /* ---- V 键快捷键（不在输入框时）---- */
  document.addEventListener('keydown', e => {
    if ((e.key === 'v' || e.key === 'V') &&
        !e.target.getAttribute('contenteditable') &&
        !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
      e.preventDefault();
      togglePanel();
    }
  });
})();

/* ===========================================
   MOBILE NAV — 移动端浮动导航按钮
   功能：
     · 点击 ☰ 按钮展开目录菜单
     · 点击菜单项平滑滚动到对应章节，并自动关闭菜单
     · 点击遮罩层关闭菜单
     · 仅在 1024px 以下生效（CSS 控制显示）
   =========================================== */
(function () {
  const btn     = document.getElementById('mobileNavBtn');
  const menu    = document.getElementById('mobileNavMenu');
  const overlay = document.getElementById('mobileNavOverlay');
  if (!btn || !menu) return;

  function openMenu() {
    menu.classList.add('open');
    overlay.classList.add('open');
    btn.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', '关闭目录');
  }
  function closeMenu() {
    menu.classList.remove('open');
    overlay.classList.remove('open');
    btn.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', '打开目录');
  }
  function toggleMenu() {
    btn.classList.contains('open') ? closeMenu() : openMenu();
  }

  btn.addEventListener('click', e => { e.stopPropagation(); toggleMenu(); });
  overlay.addEventListener('click', closeMenu);

  /* 点击菜单项：平滑滚动 + 关闭菜单 */
  menu.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (target) {
        // 考虑固定元素遮挡，向上偏移 16px
        const y = target.getBoundingClientRect().top + window.scrollY - 16;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
      closeMenu();
    });
  });
})();

/* ===========================================
   INLINE EDITOR — 内联文本编辑器
   触发方式：
     1. 鼠标悬停页面左上角热区（80×80px）→ 编辑按钮出现 → 点击
     2. 键盘快捷键 E 键（在文本框内输入时无效）
     3. 直接点击热区
   编辑模式下：
     - 所有 p、h1-h4、li、td、.abstract p、.keywords 可点击编辑
     - 编辑中的元素有绿色边框高亮
     - Ctrl+S / Cmd+S 保存到 localStorage 并导出文件
     - 再次触发 E 或点击按钮退出编辑模式
   注意：不使用 CSS ~ 兄弟选择器控制显隐（pointer-events:none 会断链）
         必须用 JS + 400ms 延时实现热区悬停效果
   =========================================== */
class ReportInlineEditor {
  constructor() {
    this.isActive   = false;
    this.storageKey = 'lab-report-edits-' + encodeURIComponent(document.title);
    this.editableSelector = [
      'h1','h2.section-title','h3','h4',
      'p:not(.no-edit)',
      'li:not(.no-edit)',
      'td:not(.no-edit)',
      '.abstract p',
      '.keywords',
      '.subtitle',
      '.journal-bar div'
    ].join(',');

    this._buildUI();
    this._bindHotzone();
    this._bindKeyboard();
    this._restoreFromStorage();
  }

  /* ---------- UI 构建 ---------- */
  _buildUI() {
    // 热区（左上角不可见触发区域）
    this.hotzone = document.createElement('div');
    this.hotzone.className = 'edit-hotzone';
    this.hotzone.title = '点击进入编辑模式';

    // 编辑切换按钮
    this.btn = document.createElement('button');
    this.btn.className = 'edit-toggle';
    this.btn.id = 'editToggle';
    this.btn.title = '编辑报告文字 (E)';
    this.btn.innerHTML = '✏️';

    // 状态提示条（编辑模式时显示在顶部）
    this.bar = document.createElement('div');
    this.bar.className = 'edit-statusbar';
    this.bar.innerHTML =
      '<span>✏️ 编辑模式 — 点击任意文字开始编辑</span>' +
      '<span class="edit-actions">' +
        '<kbd>Ctrl+S</kbd> 保存并导出 &nbsp;|&nbsp; ' +
        '<kbd>E</kbd> 退出编辑' +
      '</span>';

    document.body.prepend(this.bar);
    document.body.prepend(this.btn);
    document.body.prepend(this.hotzone);

    this.btn.addEventListener('click', () => this.toggleEditMode());
  }

  /* ---------- 热区悬停（400ms grace period，避免指针事件断链）---------- */
  _bindHotzone() {
    let hideTimer = null;

    const showBtn = () => {
      clearTimeout(hideTimer);
      this.btn.classList.add('show');
    };
    const scheduleHide = () => {
      hideTimer = setTimeout(() => {
        if (!this.isActive) this.btn.classList.remove('show');
      }, 400);
    };

    this.hotzone.addEventListener('mouseenter', showBtn);
    this.hotzone.addEventListener('mouseleave', scheduleHide);
    this.hotzone.addEventListener('click',      () => this.toggleEditMode());
    this.btn.addEventListener('mouseenter',     showBtn);
    this.btn.addEventListener('mouseleave',     scheduleHide);
  }

  /* ---------- 键盘快捷键 ---------- */
  _bindKeyboard() {
    document.addEventListener('keydown', e => {
      // E 键切换编辑模式（在 contenteditable 内输入时跳过）
      if ((e.key === 'e' || e.key === 'E') &&
          !e.target.getAttribute('contenteditable') &&
          !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
        e.preventDefault();
        this.toggleEditMode();
      }
      // Ctrl+S / Cmd+S 保存
      if ((e.ctrlKey || e.metaKey) && e.key === 's' && this.isActive) {
        e.preventDefault();
        this.saveAndExport();
      }
    });
  }

  /* ---------- 编辑模式开关 ---------- */
  toggleEditMode() {
    this.isActive ? this.exitEditMode() : this.enterEditMode();
  }

  enterEditMode() {
    this.isActive = true;
    this.btn.classList.add('active','show');
    this.btn.innerHTML = '✅';
    this.btn.title = '退出编辑模式 (E)';
    document.body.classList.add('edit-mode-on');

    // 给所有可编辑元素加上 contenteditable
    document.querySelectorAll(this.editableSelector).forEach(el => {
      // 跳过验证摘要框、代码块、图注（不应手动编辑）
      if (el.closest('.verification, .formula, figcaption, .references')) return;
      el.setAttribute('contenteditable', 'true');
      el.setAttribute('data-edit-original', el.innerHTML);
      el.classList.add('editable-active');
      // 失焦时自动存 localStorage
      el.addEventListener('blur', () => this._autosave(), { passive: true });
    });
  }

  exitEditMode() {
    this.isActive = false;
    this.btn.classList.remove('active');
    if (!this._hotzoneHovered) this.btn.classList.remove('show');
    this.btn.innerHTML = '✏️';
    this.btn.title = '编辑报告文字 (E)';
    document.body.classList.remove('edit-mode-on');

    document.querySelectorAll('[contenteditable="true"]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.classList.remove('editable-active');
    });

    this._autosave();
  }

  /* ---------- 自动保存到 localStorage ---------- */
  _autosave() {
    const edits = {};
    document.querySelectorAll('[data-edit-original]').forEach((el, i) => {
      const key = el.dataset.editOriginal ? 'el-' + i : null;
      if (key) edits[key] = { html: el.innerHTML, tag: el.tagName, index: i };
    });
    try {
      localStorage.setItem(this.storageKey, JSON.stringify({
        savedAt: new Date().toISOString(),
        body: document.querySelector('main').innerHTML
      }));
    } catch(e) { /* localStorage 不可用时静默失败 */ }
  }

  /* ---------- 从 localStorage 恢复 ---------- */
  _restoreFromStorage() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      if (!raw) return;
      const data = JSON.parse(raw);
      if (data && data.body) {
        document.querySelector('main').innerHTML = data.body;
        // 图表需要重新初始化（innerHTML 替换后 canvas 上下文丢失）
        this._reinitCharts();
        console.info('[ReportEditor] 已从本地存储恢复上次编辑，保存时间:', data.savedAt);
      }
    } catch(e) {}
  }

  /* ---------- 恢复后重新初始化 Chart.js ---------- */
  _reinitCharts() {
    // 销毁已有实例，再重建
    Object.values(Chart.instances || {}).forEach(c => c.destroy());
    // 触发自定义事件，让页面内的图表初始化代码重新运行
    document.dispatchEvent(new CustomEvent('report-editor-restored'));
  }

  /* ---------- 保存并导出 HTML 文件 ---------- */
  saveAndExport() {
    this._autosave();

    // 临时移除编辑态样式再序列化
    const wasActive = this.isActive;
    document.body.classList.remove('edit-mode-on');
    document.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.classList.remove('editable-active');
    });

    const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;

    // 恢复编辑态
    if (wasActive) {
      document.body.classList.add('edit-mode-on');
      document.querySelectorAll(this.editableSelector).forEach(el => {
        if (el.closest('.verification, .formula, figcaption, .references')) return;
        el.setAttribute('contenteditable', 'true');
        el.classList.add('editable-active');
      });
    }

    // 触发下载
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const a    = document.createElement('a');
    a.href     = URL.createObjectURL(blob);
    a.download = (document.title || 'lab-report') + '-edited.html';
    a.click();
    URL.revokeObjectURL(a.href);

    this._showToast('✅ 已保存并导出文件');
  }

  /* ---------- 轻量 Toast 提示 ---------- */
  _showToast(msg) {
    const t = document.createElement('div');
    t.className = 'edit-toast';
    t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 2200);
  }
}

// 初始化编辑器
const reportEditor = new ReportInlineEditor();
</script>

<!-- ===== 编辑器 CSS（内联，不依赖外部文件）===== -->
<style>
/* ----- 热区：左上角不可见触发区 ----- */
.edit-hotzone {
  position: fixed;
  top: 0; left: 0;
  width: 80px; height: 80px;
  z-index: 10000;
  cursor: pointer;
}

/* ----- 编辑按钮 ----- */
.edit-toggle {
  position: fixed;
  top: 14px; left: 14px;
  width: 44px; height: 44px;
  border: none;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  z-index: 10001;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 12px rgba(47,79,79,0.35);
  /* 默认隐藏；JS 通过 .show / .active 类控制 */
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease, transform 0.2s ease;
}
.edit-toggle.show,
.edit-toggle.active {
  opacity: 1;
  pointer-events: auto;
}
.edit-toggle:hover { transform: scale(1.1); }

/* 移动端始终可见 */
@media (max-width: 768px) {
  .edit-toggle {
    opacity: 1;
    pointer-events: auto;
    top: 12px;
    left: 12px;
    width: 40px;
    height: 40px;
  }
}

/* ----- 状态提示条（编辑模式时才显示）----- */
.edit-statusbar {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: var(--accent);
  color: #e8f5f5;
  font: 13px/1 "Helvetica Neue", Arial, sans-serif;
  padding: 10px 20px;
  display: none;
  justify-content: space-between;
  align-items: center;
  z-index: 9999;
  box-shadow: 0 -2px 12px rgba(0,0,0,0.15);
}
.edit-statusbar kbd {
  background: rgba(255,255,255,0.18);
  border-radius: 4px;
  padding: 2px 6px;
  font-family: monospace;
  font-size: 12px;
}
body.edit-mode-on .edit-statusbar { display: flex; }

/* ----- 编辑模式下：可编辑元素样式 ----- */
body.edit-mode-on [contenteditable]:hover {
  outline: 1.5px dashed rgba(47,79,79,0.4);
  border-radius: 3px;
  cursor: text;
}
body.edit-mode-on [contenteditable]:focus {
  outline: 2px solid var(--accent);
  border-radius: 3px;
  background: rgba(47,79,79,0.04);
}

/* ----- Toast 提示 ----- */
.edit-toast {
  position: fixed;
  bottom: 60px; left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: #1f2328;
  color: #fff;
  font: 13px/1.5 "Helvetica Neue", Arial, sans-serif;
  padding: 8px 18px;
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
  z-index: 10010;
  pointer-events: none;
  white-space: nowrap;
}
.edit-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* ----- 打印时隐藏编辑器 UI ----- */
@media print {
  .edit-hotzone, .edit-toggle, .edit-statusbar, .edit-toast { display: none !important; }
}
</style>
</body>
</html>
```

---

## 元数据字段对照

| 场景 | 左侧meta-card字段 |
|------|------------------|
| 实验课 | 作者、学号、指导教师、实验日期、提交日期、课程 |
| 科研记录 | 作者、单位、项目编号、实验日期、版本 |
| 工程报告 | 编制人、审核人、项目编号、日期、密级 |
| 竞赛展示 | 团队、参赛编号、赛事名称、日期 |

## Journal-bar左侧文字对照

| 场景 | Journal-bar左侧 |
|------|----------------|
| 实验课 | [课程名称] Lab Report |
| 科研记录 | [课题组/实验室] Research Record |
| 工程报告 | [公司/项目名] Technical Report |
| 竞赛 | [赛事名称] Competition Report |
