# 图表完整代码示例

## 示例 1：横向条形图（多类别对比，SWD 极简风）

场景：各城市销售额对比，高亮最高值

```html
<!DOCTYPE html>
<html><head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #fff; margin: 0; padding: 32px; }
  .wrap { max-width: 640px; }
  .title { font-size: 17px; font-weight: 700; color: #111827; margin-bottom: 4px; line-height: 1.3; }
  .sub { font-size: 12px; color: #9CA3AF; margin-bottom: 20px; }
  .note { font-size: 11px; color: #9CA3AF; margin-top: 10px; }
</style>
</head><body>
<div class="wrap">
  <div class="title">上海以 ¥2.3亿 领跑，超出第二名北京 34%</div>
  <div class="sub">2024年 Q3 各城市销售额 | 单位：百万元</div>
  <canvas id="c" height="220"></canvas>
  <div class="note">数据来源：销售部 2024Q3 报告</div>
</div>
<script>
const labels = ['上海','北京','广州','深圳','成都'];
const values = [230, 171, 145, 132, 98];
const highlight = Math.max(...values);
const colors = values.map(v => v === highlight ? '#2563EB' : '#D1D5DB');

Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
new Chart(document.getElementById('c'), {
  type: 'bar',
  data: { labels, datasets: [{ data: values, backgroundColor: colors, borderRadius: 4, borderSkipped: false }] },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ` ¥${ctx.raw}M` } }
    },
    scales: {
      x: { grid: { color: '#F3F4F6' }, border: { display: false }, ticks: { color: '#9CA3AF' } },
      y: { grid: { display: false }, border: { display: false }, ticks: { color: '#374151', font: { weight: '500' } } }
    }
  }
});
</script>
</body></html>
```

---

## 示例 2：折线图（趋势 + 关键点标注）

场景：月度用户增长，标注异常下跌点

```javascript
// 关键配置片段
{
  type: 'line',
  data: {
    labels: ['1月','2月','3月','4月','5月','6月'],
    datasets: [{
      data: [1200, 1450, 1380, 980, 1560, 1890],  // 4月异常下跌
      borderColor: '#2563EB',
      backgroundColor: 'rgba(37,99,235,0.06)',
      borderWidth: 2.5,
      pointRadius: [4,4,4,8,4,4],  // 4月点放大
      pointBackgroundColor: (ctx) => ctx.dataIndex === 3 ? '#DC2626' : '#2563EB',
      fill: true,
      tension: 0.3
    }]
  },
  options: {
    plugins: {
      annotation: {  // 需要 chartjs-plugin-annotation
        annotations: {
          drop: {
            type: 'label',
            xValue: '4月', yValue: 980,
            content: ['系统故障导致\n流失 400 用户'],
            color: '#DC2626', font: { size: 11 }
          }
        }
      }
    }
  }
}
```

---

## 示例 3：瀑布图（构成分析）

场景：费用拆分，从总收入到净利润

```javascript
// 瀑布图用 floating bar 实现
const data = [
  { label: '总收入', start: 0, end: 500, type: 'positive' },
  { label: '原材料', start: 500, end: 320, type: 'negative' },
  { label: '人工', start: 320, end: 210, type: 'negative' },
  { label: '运营', start: 210, end: 150, type: 'negative' },
  { label: '净利润', start: 0, end: 150, type: 'total' },
];

datasets: [{
  data: data.map(d => [d.start, d.end]),  // floating bar
  backgroundColor: data.map(d => 
    d.type === 'positive' ? '#16A34A' :
    d.type === 'negative' ? '#DC2626' : '#2563EB'
  ),
  borderRadius: 3
}]
```

---

## 示例 4：拟物条形图（薯条）

```html
<!DOCTYPE html>
<html><head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  body { font-family: 'Segoe UI', sans-serif; background:#FFFBF0; padding:32px; }
  .title { font-size:17px; font-weight:700; color:#92400E; margin-bottom:4px; }
  .sub { font-size:12px; color:#B45309; margin-bottom:20px; }
</style>
</head><body>
<div style="max-width:600px">
  <div class="title">薯条销量：大号以 4,200 份夺冠，比中号多 40%</div>
  <div class="sub">2024年门店薯条各规格月均销量 | 单位：份</div>
  <canvas id="c" height="300"></canvas>
</div>
<script>
const FRIES_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 28">
  <rect x="2" y="4" width="3.5" height="16" rx="1.5" fill="[COLOR]"/>
  <rect x="7" y="1" width="3.5" height="19" rx="1.5" fill="[COLOR]"/>
  <rect x="12" y="2" width="3.5" height="18" rx="1.5" fill="[COLOR]"/>
  <rect x="17" y="5" width="3.5" height="15" rx="1.5" fill="[COLOR]"/>
  <rect x="1" y="19" width="22" height="8" rx="2" fill="#B91C1C"/>
  <rect x="3" y="21" width="18" height="4" rx="1" fill="#DC2626"/>
</svg>`;

async function makePattern(color) {
  const svg = FRIES_SVG.replace(/\[COLOR\]/g, color);
  const url = 'data:image/svg+xml;base64,' + btoa(svg);
  return new Promise(resolve => {
    const img = new Image(32, 36);
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = 32; c.height = 36;
      c.getContext('2d').drawImage(img, 0, 0);
      resolve(c.getContext('2d').createPattern(c, 'repeat-y'));
    };
    img.src = url;
  });
}

(async () => {
  const colors = ['#F59E0B','#D97706','#B45309'];
  const patterns = await Promise.all(colors.map(makePattern));
  
  new Chart(document.getElementById('c'), {
    type: 'bar',
    data: {
      labels: ['小号(S)', '中号(M)', '大号(L)'],
      datasets: [{ 
        data: [2100, 3000, 4200],
        backgroundColor: patterns,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      plugins: { legend: { display: false },
        datalabels: false
      },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: { grid: { color: '#FEF3C7' }, border: { display: false },
          ticks: { color: '#92400E' }
        }
      }
    }
  });
})();
</script>
</body></html>
```
