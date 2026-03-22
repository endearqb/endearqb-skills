# HTML 报告模板规范 v3 — shadcn/ui 风格

## 设计语言

shadcn/ui 风格核心特征：
- **色板**：neutral 灰阶为主，强调色用 `hsl(221, 83%, 53%)`（blue-600）
- **字体**：`'Geist', 'Inter', system-ui`，严格字重层级（400/500/600/700）
- **圆角**：卡片 `8px`，按钮/徽章 `6px`，输入框 `6px`
- **阴影**：轻量 `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)`
- **边框**：`1px solid hsl(214.3, 31.8%, 91.4%)` 浅灰边框
- **间距**：4px 基础单位，常用 8/12/16/24/32px
- **支持 dark mode**：通过 `[data-theme="dark"]` 切换 CSS 变量

## 完整骨架代码

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>社区成员画像报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
/* ===== CSS Variables (shadcn/ui neutral) ===== */
:root {
  --background: hsl(0, 0%, 100%);
  --foreground: hsl(224, 71.4%, 4.1%);
  --card: hsl(0, 0%, 100%);
  --card-foreground: hsl(224, 71.4%, 4.1%);
  --muted: hsl(220, 14.3%, 95.9%);
  --muted-foreground: hsl(220, 8.9%, 46.1%);
  --border: hsl(220, 13%, 91%);
  --input: hsl(220, 13%, 91%);
  --primary: hsl(221, 83%, 53%);
  --primary-foreground: hsl(210, 40%, 98%);
  --secondary: hsl(220, 14.3%, 95.9%);
  --secondary-foreground: hsl(220.9, 39.3%, 11%);
  --accent: hsl(220, 14.3%, 95.9%);
  --accent-foreground: hsl(220.9, 39.3%, 11%);
  --destructive: hsl(0, 84.2%, 60.2%);
  --destructive-foreground: hsl(210, 40%, 98%);
  --ring: hsl(221, 83%, 53%);
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);

  /* Semantic colors */
  --success: hsl(142, 71%, 45%);
  --success-bg: hsl(142, 71%, 95%);
  --warning: hsl(38, 92%, 50%);
  --warning-bg: hsl(38, 92%, 95%);
  --danger: hsl(0, 84%, 60%);
  --danger-bg: hsl(0, 84%, 96%);
  --info: hsl(221, 83%, 53%);
  --info-bg: hsl(221, 83%, 96%);
}

[data-theme="dark"] {
  --background: hsl(224, 71.4%, 4.1%);
  --foreground: hsl(210, 20%, 98%);
  --card: hsl(224, 71.4%, 6%);
  --card-foreground: hsl(210, 20%, 98%);
  --muted: hsl(215, 27.9%, 16.9%);
  --muted-foreground: hsl(217.9, 10.6%, 64.9%);
  --border: hsl(215, 27.9%, 16.9%);
  --primary: hsl(217, 91%, 60%);
  --secondary: hsl(215, 27.9%, 16.9%);
  --success-bg: hsl(142, 71%, 10%);
  --warning-bg: hsl(38, 92%, 10%);
  --danger-bg: hsl(0, 84%, 10%);
  --info-bg: hsl(221, 83%, 10%);
}

/* ===== Reset & Base ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--background);
  color: var(--foreground);
  font-family: 'Geist', 'Inter', -apple-system, system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

/* ===== Layout ===== */
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }
.page-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 24px 0 20px; border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.page-title { font-size: 20px; font-weight: 600; letter-spacing: -0.025em; }
.page-meta { font-size: 12px; color: var(--muted-foreground); margin-top: 4px; }
.theme-toggle {
  display: flex; align-items: center; gap: 6px;
  background: var(--secondary); border: 1px solid var(--border);
  border-radius: 6px; padding: 6px 12px; cursor: pointer;
  font-size: 12px; color: var(--muted-foreground);
  transition: background 0.15s;
}
.theme-toggle:hover { background: var(--muted); }

/* ===== Alert Banner ===== */
.alert {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 12px 16px; border-radius: var(--radius);
  border: 1px solid; margin-bottom: 16px; font-size: 13px;
}
.alert-warning { background: var(--warning-bg); border-color: var(--warning); color: hsl(38,92%,30%); }
.alert-info { background: var(--info-bg); border-color: var(--info); color: hsl(221,83%,30%); }
[data-theme="dark"] .alert-warning { color: var(--warning); }
[data-theme="dark"] .alert-info { color: var(--primary); }
.alert-icon { font-size: 15px; flex-shrink: 0; margin-top: 1px; }

/* ===== Stats Row ===== */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin-bottom: 24px; }
.stat-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  box-shadow: var(--shadow);
}
.stat-value { font-size: 28px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
.stat-label { font-size: 11px; color: var(--muted-foreground); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
.stat-value.blue { color: var(--primary); }
.stat-value.green { color: var(--success); }
.stat-value.red { color: var(--danger); }

/* ===== Section ===== */
.section { margin-bottom: 32px; }
.section-header { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.section-title { font-size: 15px; font-weight: 600; }
.section-badge {
  font-size: 11px; background: var(--muted); color: var(--muted-foreground);
  padding: 2px 8px; border-radius: 20px; font-weight: 500;
}

/* ===== Content Summary ===== */
.topics-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; margin-bottom: 20px; }
.topic-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  box-shadow: var(--shadow); transition: box-shadow 0.15s;
}
.topic-card:hover { box-shadow: var(--shadow-md); }
.topic-title { font-size: 13px; font-weight: 600; margin-bottom: 6px; }
.topic-desc { font-size: 12px; color: var(--muted-foreground); line-height: 1.6; margin-bottom: 10px; }
.topic-footer { display: flex; align-items: center; justify-content: space-between; }
.topic-participants { font-size: 11px; color: var(--muted-foreground); }
.heat-bar { display: flex; align-items: center; gap: 6px; }
.heat-fill { height: 4px; border-radius: 2px; background: var(--primary); opacity: 0.7; }

.highlights-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.highlight-item {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 14px 16px;
  border-left: 3px solid var(--primary);
  box-shadow: var(--shadow);
}
.highlight-sender { font-size: 12px; font-weight: 600; color: var(--primary); margin-bottom: 6px; }
.highlight-content { font-size: 13px; line-height: 1.65; color: var(--foreground); font-style: italic; }
.highlight-tags { margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap; }

.consensus-disputes { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
@media (max-width: 640px) { .consensus-disputes { grid-template-columns: 1fr; } }
.cd-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; box-shadow: var(--shadow); }
.cd-title { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted-foreground); margin-bottom: 10px; }
.consensus-item { font-size: 12px; padding: 6px 0; border-bottom: 1px solid var(--border); color: var(--foreground); }
.consensus-item:last-child { border-bottom: none; }
.dispute-item { margin-bottom: 10px; }
.dispute-topic { font-size: 12px; font-weight: 600; margin-bottom: 4px; }
.dispute-sides { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.dispute-side { background: var(--muted); border-radius: 6px; padding: 8px; font-size: 11px; color: var(--muted-foreground); }
.dispute-side-label { font-weight: 600; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--primary); margin-bottom: 2px; }

.action-list { display: flex; flex-direction: column; gap: 8px; }
.action-item {
  display: flex; align-items: flex-start; gap: 10px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 10px 14px;
  box-shadow: var(--shadow); font-size: 12px;
}
.action-icon { color: var(--warning); flex-shrink: 0; font-size: 14px; }
.action-proposer { font-weight: 600; color: var(--primary); margin-right: 4px; }
.action-target { color: var(--muted-foreground); margin-left: 4px; }

/* ===== Member Cards ===== */
.members-viewport { position: relative; overflow: hidden; }
.member-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }

/* 虚拟滚动容器 */
.virtual-container { position: relative; }
.virtual-spacer-top { background: transparent; }
.virtual-spacer-bottom { background: transparent; }

.member-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  box-shadow: var(--shadow); cursor: pointer;
  transition: box-shadow 0.15s, border-color 0.15s;
}
.member-card:hover { box-shadow: var(--shadow-md); border-color: var(--ring); }
.member-card-header { padding: 14px 16px 10px; }
.member-rank-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.member-rank { font-size: 11px; font-weight: 600; color: var(--muted-foreground); text-transform: uppercase; letter-spacing: 0.06em; }
.member-rank.gold { color: hsl(38,92%,40%); }
.member-rank.silver { color: hsl(0,0%,50%); }
.member-rank.bronze { color: hsl(25,80%,45%); }
.member-name { font-size: 14px; font-weight: 600; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.member-score-row { display: flex; align-items: baseline; gap: 6px; margin-bottom: 8px; }
.member-score { font-size: 30px; font-weight: 700; letter-spacing: -0.04em; color: var(--primary); line-height: 1; }
.member-score-label { font-size: 11px; color: var(--muted-foreground); }
.badges-row { display: flex; flex-wrap: wrap; gap: 4px; }
.badge {
  font-size: 11px; padding: 2px 8px; border-radius: 6px; font-weight: 500;
  background: var(--secondary); color: var(--secondary-foreground);
  border: 1px solid var(--border);
}
.badge-risk-high { background: var(--danger-bg); color: var(--danger); border-color: var(--danger); }
.badge-risk-medium { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
.badge-risk-low { background: var(--success-bg); color: var(--success); border-color: var(--success); }

/* 展开区域（默认隐藏） */
.member-card-expand {
  border-top: 1px solid var(--border);
  padding: 12px 16px 14px;
  display: none;
  background: var(--muted);
  animation: slideDown 0.2s ease;
}
.member-card.expanded .member-card-expand { display: block; }
@keyframes slideDown { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

.mini-bars { display: flex; flex-direction: column; gap: 5px; margin-bottom: 10px; }
.mini-bar-row { display: flex; align-items: center; gap: 8px; }
.mini-bar-label { width: 52px; font-size: 11px; color: var(--muted-foreground); text-align: right; flex-shrink: 0; }
.mini-bar-track { flex: 1; height: 5px; background: var(--border); border-radius: 10px; overflow: hidden; }
.mini-bar-fill { height: 100%; border-radius: 10px; transition: width 0.4s ease; }
.mini-bar-value { width: 22px; font-size: 10px; color: var(--muted-foreground); text-align: right; flex-shrink: 0; }
.member-quote {
  font-size: 12px; color: var(--muted-foreground); font-style: italic;
  border-left: 2px solid var(--border); padding-left: 10px; line-height: 1.6;
  margin-top: 6px;
}
.risk-factors { margin-top: 8px; }
.risk-factor-item { font-size: 11px; color: var(--muted-foreground); padding: 2px 0; }

/* ===== Radar Charts ===== */
.radar-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.radar-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; box-shadow: var(--shadow); }
.radar-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.radar-score { font-size: 11px; color: var(--primary); font-weight: 600; margin-bottom: 12px; }

/* ===== KOL Cards ===== */
.kol-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.kol-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  box-shadow: var(--shadow); position: relative; overflow: hidden;
}
.kol-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--primary); }
.kol-name { font-size: 14px; font-weight: 600; margin-bottom: 2px; }
.kol-score { font-size: 24px; font-weight: 700; color: var(--primary); letter-spacing: -0.03em; margin-bottom: 8px; }
.kol-signal { font-size: 12px; color: var(--muted-foreground); padding: 3px 0; display: flex; align-items: center; gap: 6px; }
.kol-signal::before { content: '•'; color: var(--primary); }
.kol-domains { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
.kol-recommend { font-size: 11px; background: var(--info-bg); color: var(--primary); border-radius: 6px; padding: 6px 10px; margin-top: 10px; border: 1px solid var(--primary); opacity: 0.8; }

/* ===== Charts ===== */
.chart-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.chart-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; box-shadow: var(--shadow); }
.chart-title { font-size: 12px; font-weight: 600; color: var(--muted-foreground); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 14px; }

/* ===== Knowledge Coverage ===== */
.coverage-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.coverage-item {
  display: flex; flex-direction: column; gap: 2px;
  padding: 8px 12px; border-radius: 6px;
  border: 1px solid var(--border); font-size: 12px; font-weight: 500;
}
.coverage-item.covered { background: var(--success-bg); border-color: var(--success); color: hsl(142,50%,30%); }
.coverage-item.weak { background: var(--warning-bg); border-color: var(--warning); color: hsl(38,80%,30%); }
.coverage-item.gap { background: var(--danger-bg); border-color: var(--danger); color: hsl(0,60%,40%); }
[data-theme="dark"] .coverage-item.covered { color: var(--success); }
[data-theme="dark"] .coverage-item.weak { color: var(--warning); }
[data-theme="dark"] .coverage-item.gap { color: var(--danger); }
.coverage-experts { font-size: 11px; font-weight: 400; opacity: 0.75; }
.coverage-legend { display: flex; gap: 16px; margin-top: 10px; font-size: 11px; color: var(--muted-foreground); }
.legend-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }

/* ===== Asset List ===== */
.asset-list { display: flex; flex-direction: column; gap: 8px; }
.asset-item { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 12px 16px; display: flex; gap: 12px; align-items: flex-start; box-shadow: var(--shadow); }
.asset-rank { font-size: 12px; font-weight: 700; color: var(--muted-foreground); min-width: 24px; }
.asset-rank.top3 { color: hsl(38,92%,40%); }
.asset-body { flex: 1; min-width: 0; }
.asset-title-text { font-size: 13px; font-weight: 500; margin-bottom: 2px; }
.asset-url { font-size: 11px; color: var(--primary); text-decoration: none; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }
.asset-summary-text { font-size: 11px; color: var(--muted-foreground); margin-top: 4px; line-height: 1.5; }
.asset-meta-row { display: flex; gap: 8px; margin-top: 4px; font-size: 11px; color: var(--muted-foreground); }
.status-badge { font-size: 10px; padding: 2px 7px; border-radius: 4px; font-weight: 500; white-space: nowrap; flex-shrink: 0; }
.status-success { background: var(--success-bg); color: var(--success); }
.status-failed { background: var(--danger-bg); color: var(--danger); }

/* ===== Health Box ===== */
.health-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.health-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; box-shadow: var(--shadow); }
.health-card-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted-foreground); margin-bottom: 8px; }
.health-card-content { font-size: 12px; line-height: 1.7; color: var(--foreground); }
.layer-names { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }

/* ===== Skeleton ===== */
.skeleton { background: var(--muted); border-radius: 4px; animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.skeleton-card { height: 140px; border-radius: var(--radius); }
.skeleton-text-short { height: 12px; width: 60%; margin-bottom: 6px; }
.skeleton-text-long { height: 12px; width: 90%; margin-bottom: 6px; }

/* ===== Tabs ===== */
.tabs { display: flex; border-bottom: 1px solid var(--border); margin-bottom: 16px; gap: 0; }
.tab-btn {
  padding: 8px 16px; font-size: 13px; font-weight: 500; cursor: pointer;
  border: none; background: none; color: var(--muted-foreground);
  border-bottom: 2px solid transparent; margin-bottom: -1px;
  transition: color 0.15s, border-color 0.15s;
}
.tab-btn.active { color: var(--foreground); border-bottom-color: var(--foreground); }
.tab-btn:hover { color: var(--foreground); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .container { padding: 16px; }
  .page-header { flex-direction: column; gap: 12px; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .member-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="page-header">
    <div>
      <div class="page-title">社区成员画像报告</div>
      <div class="page-meta" id="meta-info">加载中...</div>
    </div>
    <button class="theme-toggle" onclick="toggleTheme()">🌙 切换主题</button>
  </div>

  <!-- Alerts -->
  <div id="alerts-container"></div>

  <!-- Skeleton loading (shown until data renders) -->
  <div id="skeleton-screen">
    <div class="stats-row">
      <div class="skeleton skeleton-card" style="height:72px"></div>
      <div class="skeleton skeleton-card" style="height:72px"></div>
      <div class="skeleton skeleton-card" style="height:72px"></div>
      <div class="skeleton skeleton-card" style="height:72px"></div>
    </div>
    <div class="member-grid">
      <div class="skeleton skeleton-card"></div>
      <div class="skeleton skeleton-card"></div>
      <div class="skeleton skeleton-card"></div>
    </div>
  </div>

  <!-- Main content (hidden until ready) -->
  <div id="main-content" style="display:none">

    <!-- Stats Row -->
    <div class="stats-row" id="stats-row"></div>

    <!-- ① Content Summary -->
    <div class="section" id="section-summary">
      <div class="section-header">
        <span class="section-title">💬 聊天内容总结</span>
        <span class="section-badge" id="badge-topics">-</span>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('topics')">核心议题</button>
        <button class="tab-btn" onclick="switchTab('highlights')">精华发言</button>
        <button class="tab-btn" onclick="switchTab('consensus')">共识与分歧</button>
        <button class="tab-btn" onclick="switchTab('actions')">行动项</button>
      </div>

      <div id="tab-topics" class="tab-panel active">
        <div class="topics-grid" id="topics-grid"></div>
      </div>
      <div id="tab-highlights" class="tab-panel">
        <div class="highlights-list" id="highlights-list"></div>
      </div>
      <div id="tab-consensus" class="tab-panel">
        <div class="consensus-disputes" id="consensus-disputes"></div>
      </div>
      <div id="tab-actions" class="tab-panel">
        <div class="action-list" id="action-list"></div>
      </div>
    </div>

    <!-- ② Member Ranking -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">🏆 成员综合影响力排行</span>
        <span class="section-badge" id="badge-members">-</span>
        <span style="font-size:11px;color:var(--muted-foreground);margin-left:auto">点击卡片展开详情</span>
      </div>
      <!-- 虚拟滚动包装器 -->
      <div id="member-list-root"></div>
    </div>

    <!-- ④ KOL -->
    <div class="section" id="section-kol" style="display:none">
      <div class="section-header"><span class="section-title">⭐ KOL 候选推荐</span></div>
      <div class="kol-grid" id="kol-grid"></div>
    </div>

    <!-- ⑥ Knowledge Coverage -->
    <div class="section" id="section-coverage">
      <div class="section-header"><span class="section-title">🗺️ 知识领域覆盖</span></div>
      <div class="coverage-grid" id="coverage-grid"></div>
      <div class="coverage-legend">
        <span><span class="legend-dot" style="background:var(--success)"></span>覆盖充分（≥2位专家）</span>
        <span><span class="legend-dot" style="background:var(--warning)"></span>覆盖薄弱（1位专家）</span>
        <span><span class="legend-dot" style="background:var(--danger)"></span>领域空白</span>
      </div>
    </div>

    <!-- ⑦ Assets -->
    <div class="section" id="section-assets" style="display:none">
      <div class="section-header"><span class="section-title">🔗 传播资源热榜</span></div>
      <div class="asset-list" id="asset-list"></div>
    </div>

    <!-- ⑧ Role Distribution -->
    <div class="section">
      <div class="section-header"><span class="section-title">📊 社区生态分布</span></div>
      <div class="chart-grid">
        <div class="chart-card"><div class="chart-title">角色分布</div><canvas id="role-chart" height="220"></canvas></div>
        <div class="chart-card"><div class="chart-title">活跃度分布</div><canvas id="activity-chart" height="220"></canvas></div>
      </div>
    </div>

    <!-- ⑨ Community Health -->
    <div class="section">
      <div class="section-header"><span class="section-title">💡 社区健康评估</span></div>
      <div class="health-grid" id="health-grid"></div>
    </div>

  </div><!-- /main-content -->
</div><!-- /container -->

<script>
// ========================================
// 数据注入点
const DATA = INJECT_JSON_PLACEHOLDER;
// ========================================

// Chart.js 全局配置（适配 shadcn 风格）
function getChartDefaults() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    gridColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)',
    textColor: isDark ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.5)',
  };
}

// ===== 主题切换 =====
function toggleTheme() {
  const html = document.documentElement;
  html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
}

// ===== Tab 切换 =====
function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach((b,i) => {
    const tabNames = ['topics','highlights','consensus','actions'];
    b.classList.toggle('active', tabNames[i] === name);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.toggle('active', p.id === 'tab-' + name);
  });
}

// ===== 成员卡片展开 =====
function toggleCard(card) {
  card.classList.toggle('expanded');
}

// ===== 虚拟滚动 =====
class VirtualScroller {
  constructor(container, items, renderFn, itemHeight = 180, cols = 3) {
    this.container = container;
    this.items = items;
    this.renderFn = renderFn;
    this.itemH = itemHeight;
    this.cols = cols;
    this.rendered = new Map();
    this.init();
  }
  init() {
    const rows = Math.ceil(this.items.length / this.cols);
    const totalH = rows * (this.itemH + 12);

    this.container.style.position = 'relative';
    this.container.style.height = totalH + 'px';

    // 初始渲染可见区域
    this.update();
    window.addEventListener('scroll', () => this.update(), { passive: true });
    window.addEventListener('resize', () => { this.cols = this.getCols(); this.update(); });
  }
  getCols() {
    const w = this.container.offsetWidth;
    if (w < 600) return 1;
    if (w < 900) return 2;
    return 3;
  }
  update() {
    const scrollY = window.scrollY;
    const viewH = window.innerHeight;
    const rect = this.container.getBoundingClientRect();
    const top = rect.top + scrollY;

    const visibleTop = Math.max(0, scrollY - top - viewH);
    const visibleBot = scrollY - top + viewH * 2;

    const rowH = this.itemH + 12;
    const startRow = Math.max(0, Math.floor(visibleTop / rowH));
    const endRow = Math.min(Math.ceil(this.items.length / this.cols), Math.ceil(visibleBot / rowH));

    const startIdx = startRow * this.cols;
    const endIdx = Math.min(this.items.length, endRow * this.cols);

    // 移除不可见的
    for (const [idx, el] of this.rendered) {
      if (idx < startIdx || idx >= endIdx) {
        el.remove();
        this.rendered.delete(idx);
      }
    }

    // 渲染新的
    for (let i = startIdx; i < endIdx; i++) {
      if (this.rendered.has(i)) continue;
      const row = Math.floor(i / this.cols);
      const col = i % this.cols;
      const colWidth = 100 / this.cols;
      const el = document.createElement('div');
      el.style.cssText = `
        position: absolute;
        top: ${row * rowH}px;
        left: calc(${col * colWidth}% + ${col > 0 ? 6 : 0}px);
        width: calc(${colWidth}% - ${this.cols > 1 ? 6 : 0}px);
      `;
      el.innerHTML = this.renderFn(this.items[i], i);
      el.querySelector('.member-card')?.addEventListener('click', e => toggleCard(e.currentTarget));
      this.container.appendChild(el);
      this.rendered.set(i, el);
    }
  }
}

// ===== 渲染函数 =====
const DIM_KEYS = ['activity','content_quality','interaction_influence','professional_authority','community_stickiness'];
const DIM_LABELS = ['活跃度','内容质量','互动影响','专业权威','社区粘性'];
const DIM_COLORS = ['hsl(221,83%,53%)','hsl(142,71%,45%)','hsl(262,80%,60%)','hsl(38,92%,50%)','hsl(199,89%,48%)'];
const RISK_LABEL = { high:'高风险', medium:'中风险', low:'健康' };
const RISK_CLASS = { high:'badge-risk-high', medium:'badge-risk-medium', low:'badge-risk-low' };
const RANK_CLASS = (i) => i === 0 ? 'gold' : i === 1 ? 'silver' : i === 2 ? 'bronze' : '';

function renderMemberCard(m, i) {
  const rk = m.churn_risk_level || 'low';
  return `
    <div class="member-card">
      <div class="member-card-header">
        <div class="member-rank-row">
          <span class="member-rank ${RANK_CLASS(i)}">#${i+1}</span>
        </div>
        <div class="member-name" title="${m.nickname}">${m.nickname}</div>
        <div class="member-score-row">
          <span class="member-score">${m.scores.composite}</span>
          <span class="member-score-label">综合分</span>
        </div>
        <div class="badges-row">
          ${m.roles.map(r => `<span class="badge">${r}</span>`).join('')}
          <span class="badge ${RISK_CLASS[rk]}">${RISK_LABEL[rk]}</span>
        </div>
      </div>
      <div class="member-card-expand">
        <div class="mini-bars">
          ${DIM_KEYS.map((k,j) => `
            <div class="mini-bar-row">
              <span class="mini-bar-label">${DIM_LABELS[j]}</span>
              <div class="mini-bar-track">
                <div class="mini-bar-fill" style="width:${m.scores[k]||0}%;background:${DIM_COLORS[j]}"></div>
              </div>
              <span class="mini-bar-value">${m.scores[k]||0}</span>
            </div>`).join('')}
        </div>
        ${m.highlights?.length ? `<div class="member-quote">"${m.highlights[0]}"</div>` : ''}
        ${m.risk_factors?.length ? `
          <div class="risk-factors">${m.risk_factors.map(f =>
            `<div class="risk-factor-item">• ${f}</div>`).join('')}
          </div>` : ''}
        ${m.tech_domains?.length ? `
          <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">
            ${m.tech_domains.map(d => `<span class="badge" style="font-size:10px">${d}</span>`).join('')}
          </div>` : ''}
      </div>
    </div>`;
}

// ===== 主渲染流程 =====
function render() {
  const D = DATA;
  const members = D.members.sort((a,b) => b.scores.composite - a.scores.composite);
  const health = D.community_health;
  const meta = D.analysis_meta;
  const summary = D.content_summary || {};

  // 隐藏骨架，显示内容
  document.getElementById('skeleton-screen').style.display = 'none';
  document.getElementById('main-content').style.display = '';

  // --- Alerts ---
  const alertsHtml = [];
  if (!meta.has_timestamp) {
    alertsHtml.push(`<div class="alert alert-warning"><span class="alert-icon">⚠️</span><span>记录无时间信息，时序类指标已跳过，权重已自动调整（活跃度↓5% · 内容质量↑5% · 互动影响↑5% · 专业权威↑5%）</span></div>`);
  }
  if (meta.spam_messages_filtered > 0) {
    alertsHtml.push(`<div class="alert alert-info"><span class="alert-icon">ℹ️</span><span>已过滤垃圾/无效消息 <strong>${meta.spam_messages_filtered}</strong> 条，不计入成员评分</span></div>`);
  }
  document.getElementById('alerts-container').innerHTML = alertsHtml.join('');

  // --- Meta ---
  document.getElementById('meta-info').textContent =
    `生成时间：${meta.generated_at}  ·  消息总数：${meta.total_messages}  ·  成员：${meta.member_count}  ·  模式：${meta.weight_mode}`;

  // --- Stats ---
  const riskC = {high:0,medium:0,low:0};
  members.forEach(m => riskC[m.churn_risk_level||'low']++);
  document.getElementById('stats-row').innerHTML = [
    { label:'成员总数', value: meta.member_count, cls:'' },
    { label:'有效消息', value: meta.total_messages - meta.spam_messages_filtered, cls:'blue' },
    { label:'KOL候选', value: health.kol_candidates?.length||0, cls:'blue' },
    { label:'高风险成员', value: riskC.high, cls: riskC.high > 0 ? 'red' : '' },
    { label:'话题数', value: health.topic_clusters?.length||0, cls:'' },
  ].map(s => `<div class="stat-card"><div class="stat-value ${s.cls}">${s.value}</div><div class="stat-label">${s.label}</div></div>`).join('');

  // ====== 内容总结渲染 ======
  // 议题
  document.getElementById('badge-topics').textContent = `${summary.topics?.length||0} 个议题`;
  document.getElementById('topics-grid').innerHTML = (summary.topics||[]).map(t => `
    <div class="topic-card">
      <div class="topic-title">${t.title}</div>
      <div class="topic-desc">${t.description}</div>
      <div class="topic-footer">
        <span class="topic-participants">👥 ${t.participants?.slice(0,3).join('、')||''}${t.participants?.length>3?' 等':''}（${t.participants?.length||0}人参与）</span>
        <div class="heat-bar">
          <div class="mini-bar-track" style="width:50px">
            <div class="heat-fill" style="width:${t.heat_score||50}%"></div>
          </div>
          <span style="font-size:10px;color:var(--muted-foreground)">${t.message_count}条</span>
        </div>
      </div>
    </div>`).join('');

  // 精华发言
  const valueColors = { '技术洞察':'var(--primary)', '精准提问':'var(--success)', '有效解答':'var(--warning)', '引发讨论':'var(--danger)' };
  document.getElementById('highlights-list').innerHTML = (summary.highlights||[]).map(h => `
    <div class="highlight-item">
      <div class="highlight-sender">${h.sender}</div>
      <div class="highlight-content">${h.content}</div>
      <div class="highlight-tags">
        <span class="badge" style="border-color:${valueColors[h.value_tag]||'var(--border)'};color:${valueColors[h.value_tag]||'inherit'}">${h.value_tag}</span>
        ${h.replies_triggered > 0 ? `<span class="badge">引发 ${h.replies_triggered} 条回复</span>` : ''}
      </div>
    </div>`).join('');

  // 共识与分歧
  const consensusHtml = `
    <div class="cd-card">
      <div class="cd-title">✅ 共识</div>
      ${(summary.consensus||[]).map(c => `<div class="consensus-item">• ${c}</div>`).join('') || '<div class="consensus-item" style="color:var(--muted-foreground)">暂无明确共识</div>'}
    </div>
    <div class="cd-card">
      <div class="cd-title">⚡ 分歧</div>
      ${(summary.disputes||[]).map(d => `
        <div class="dispute-item">
          <div class="dispute-topic">${d.topic}</div>
          <div class="dispute-sides">
            <div class="dispute-side"><div class="dispute-side-label">观点A（${d.side_a.supporters?.join('、')||''}）</div>${d.side_a.position}</div>
            <div class="dispute-side"><div class="dispute-side-label">观点B（${d.side_b.supporters?.join('、')||''}）</div>${d.side_b.position}</div>
          </div>
        </div>`).join('') || '<div style="font-size:12px;color:var(--muted-foreground)">暂无明显分歧</div>'}
    </div>`;
  document.getElementById('consensus-disputes').innerHTML = consensusHtml;

  // 行动项
  document.getElementById('action-list').innerHTML = (summary.action_items||[]).map(a => `
    <div class="action-item">
      <span class="action-icon">📌</span>
      <div><span class="action-proposer">${a.proposer}</span>${a.action}${a.target ? `<span class="action-target">→ ${a.target}</span>` : ''}</div>
    </div>`).join('') || '<div style="font-size:12px;color:var(--muted-foreground);padding:12px 0">本段记录中未发现明确行动项</div>';

  // ====== 成员列表（虚拟滚动） ======
  document.getElementById('badge-members').textContent = `${members.length} 人`;
  const root = document.getElementById('member-list-root');

  if (members.length > 30) {
    // 启用虚拟滚动
    new VirtualScroller(root, members, renderMemberCard, 220, 3);
  } else {
    // 直接渲染
    root.innerHTML = `<div class="member-grid">${members.map((m,i) => renderMemberCard(m,i)).join('')}</div>`;
    root.querySelectorAll('.member-card').forEach(c => c.addEventListener('click', () => toggleCard(c)));
  }

  // ====== KOL ======
  const kols = health.kol_candidates || [];
  if (kols.length) {
    document.getElementById('section-kol').style.display = '';
    document.getElementById('kol-grid').innerHTML = kols.map(k => `
      <div class="kol-card">
        <div class="kol-name">${k.nickname}</div>
        <div class="kol-score">${k.composite_score}</div>
        ${k.kol_signals.map(s => `<div class="kol-signal">${s}</div>`).join('')}
        <div class="kol-domains">${(k.tech_domains||[]).map(d => `<span class="badge" style="font-size:10px">${d}</span>`).join('')}</div>
        ${k.recommended_for ? `<div class="kol-recommend">💡 ${k.recommended_for}</div>` : ''}
      </div>`).join('');
  }

  // ====== Coverage ======
  const cov = health.knowledge_coverage || {};
  document.getElementById('coverage-grid').innerHTML = Object.entries(cov).map(([d,info]) => `
    <div class="coverage-item ${info.level}">
      ${d}
      <span class="coverage-experts">${info.experts?.length ? info.experts.slice(0,2).join('、') : '暂无专家'}</span>
    </div>`).join('');

  // ====== Assets ======
  const assets = health.top_assets || [];
  if (assets.length) {
    document.getElementById('section-assets').style.display = '';
    document.getElementById('asset-list').innerHTML = assets.slice(0,10).map((a,i) => `
      <div class="asset-item">
        <div class="asset-rank ${i<3?'top3':''}">#${i+1}</div>
        <div class="asset-body">
          <div class="asset-title-text">${a.title||a.url}</div>
          <a class="asset-url" href="${a.url}" target="_blank">${a.url}</a>
          ${a.summary ? `<div class="asset-summary-text">${a.summary}</div>` : ''}
          <div class="asset-meta-row"><span>🔁 ${a.share_count} 次转发</span><span>${(a.shared_by||[]).slice(0,3).join('、')}</span></div>
        </div>
        <span class="status-badge ${a.fetch_status==='success'?'status-success':'status-failed'}">${a.fetch_status==='success'?'✓ 已抓取':'✗ '+a.fetch_status}</span>
      </div>`).join('');
  }

  // ====== Role & Activity Charts ======
  const roleC = {};
  members.forEach(m => { const r=m.roles[0]; roleC[r]=(roleC[r]||0)+1; });
  const { textColor } = getChartDefaults();
  new Chart(document.getElementById('role-chart'), {
    type:'doughnut',
    data:{ labels:Object.keys(roleC), datasets:[{ data:Object.values(roleC), backgroundColor:['hsl(221,83%,53%)','hsl(142,71%,45%)','hsl(199,89%,48%)','hsl(38,92%,50%)','hsl(262,80%,60%)','hsl(0,84%,60%)','hsl(160,60%,45%)','hsl(25,80%,45%)'], borderWidth:0 }]},
    options:{ plugins:{ legend:{ position:'right', labels:{ color:textColor, font:{size:11}, boxWidth:10 }}}, cutout:'50%' }
  });

  const bkt=[0,0,0,0,0];
  members.forEach(m => { bkt[Math.min(4,Math.floor((m.stats.message_count||0)/3))]++; });
  new Chart(document.getElementById('activity-chart'), {
    type:'bar',
    data:{ labels:['1-2条','3-5条','6-9条','10-15条','16条+'], datasets:[{ data:bkt, backgroundColor:'hsl(221,83%,53%)', borderRadius:4, borderSkipped:false }]},
    options:{ plugins:{legend:{display:false}}, scales:{ y:{ticks:{color:textColor},grid:{color:getChartDefaults().gridColor}}, x:{ticks:{color:textColor},grid:{display:false}} } }
  });

  // ====== Health ======
  const cl = health.core_periphery_layers || {};
  document.getElementById('health-grid').innerHTML = [
    { label:'活跃趋势', content: health.activity_trend||'未知' },
    { label:'主要话题', content: (health.topic_clusters||[]).join('、') },
    { label:'核心层', content: `<div class="layer-names">${(cl.core||[]).map(n=>`<span class="badge">${n}</span>`).join('')}</div>` },
    { label:'活跃层', content: `<div class="layer-names">${(cl.active||[]).map(n=>`<span class="badge">${n}</span>`).join('')}</div>` },
    { label:'健康评估', content: health.health_notes||'' },
  ].map(h => `
    <div class="health-card">
      <div class="health-card-label">${h.label}</div>
      <div class="health-card-content">${h.content}</div>
    </div>`).join('');
}

// 启动：骨架屏显示后异步渲染
window.addEventListener('DOMContentLoaded', () => {
  requestAnimationFrame(() => setTimeout(render, 50));
});
</script>
</body>
</html>
```

## 数据注入方式

将 `report.json` 序列化后替换 `INJECT_JSON_PLACEHOLDER`：

```python
html = template.replace('INJECT_JSON_PLACEHOLDER', json.dumps(data, ensure_ascii=False))
```

## content_summary 字段说明

生成 JSON 时需要在 `community_health` 同级填充 `content_summary`：

```json
{
  "content_summary": {
    "topics": [
      { "title": "龙虾 vs CC 工具链", "description": "...", "participants": ["Jackie Mao","fengzeng"], "message_count": 18, "heat_score": 85 }
    ],
    "highlights": [
      { "sender": "Patch", "content": "原文...", "value_tag": "技术洞察", "replies_triggered": 0 }
    ],
    "consensus": ["普通人用CC门槛较高"],
    "disputes": [
      { "topic": "OpenClaw是否有独特价值", "side_a": { "position": "有，给CC加上IM渠道", "supporters": ["1337"] }, "side_b": { "position": "没发现它能干CC不能干的事", "supporters": ["fengzeng"] } }
    ],
    "action_items": [
      { "proposer": "Ray.", "action": "周日虾友局活动，邀请有OpenClaw经验的人分享", "target": "杭州群友" }
    ]
  }
}
```
