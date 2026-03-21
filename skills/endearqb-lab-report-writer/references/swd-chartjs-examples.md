# Storytelling with Data 原则 — Chart.js实现示例

## 核心原则速查

| SWD原则 | 在Chart.js中的实现 |
|---------|-------------------|
| 选择合适图表类型 | 见"图表类型选择矩阵" |
| 去除图表垃圾 | `legend: false`、无边框、极淡网格 |
| 数据墨水比最大化 | 只保留必要元素 |
| 用颜色强调重点 | 主色`#2f4f4f`，其余灰色 |
| 描述性标题 | 写在`<figcaption>`，而非chart内 |
| 直接标注优于图例 | 用`plugin: datalabels`或手动SVG标注 |

---

## 图表类型选择矩阵

| 我想表达… | 推荐图表 | Chart.js type |
|-----------|----------|---------------|
| 两个变量的关系 | 散点图 | `scatter` |
| 随时间/条件变化的趋势 | 折线图 | `line` |
| 不同组之间的数量对比 | 水平柱状图 | `bar` (horizontal) |
| 一系列测量值的分布 | 直方图（用bar模拟）| `bar` |
| 占比（慎用，≤5类） | 圆环图 | `doughnut` |
| 多变量比较 | 雷达图 | `radar` |
| 误差范围 | 折线图+error bar | `line` + 自定义 |

**原则：先用散点/折线，能说明问题就不用饼图。**

---

## 完整配置模板集

### 1. 折线图（实验数据趋势）

```javascript
new Chart(ctx, {
  type: 'line',
  data: {
    labels: [/* x轴标签，如时间/条件 */],
    datasets: [
      {
        label: '实验组',
        data: [/* 数据数组 */],
        borderColor: '#2f4f4f',
        backgroundColor: 'rgba(47,79,79,0.08)',
        borderWidth: 2.5,
        pointRadius: 5,
        pointHoverRadius: 7,
        tension: 0.3,
        fill: true
      },
      {
        label: '对照组',
        data: [/* 对照数据 */],
        borderColor: '#aab0b8',          // 灰色：次要系列
        backgroundColor: 'transparent',
        borderWidth: 1.5,
        borderDash: [5, 4],              // 虚线区分
        pointRadius: 3,
        tension: 0.3
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },       // 禁用图例（用figcaption标注代替）
      tooltip: {
        callbacks: {
          label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}`
        }
      }
    },
    scales: {
      x: {
        title: { display: true, text: '[x轴单位]', color: '#5c6570' },
        grid: { display: false },
        border: { display: false }
      },
      y: {
        title: { display: true, text: '[y轴单位]', color: '#5c6570' },
        grid: { color: '#f0ece2', lineWidth: 1 },
        border: { display: false },
        beginAtZero: false
      }
    }
  }
});
```

### 2. 水平柱状图（多组对比）

```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [/* 分组标签 */],
    datasets: [{
      label: '[指标名]',
      data: [/* 数据 */],
      backgroundColor: [
        '#2f4f4f',    // 第一个（重点）深色
        '#7a9e9f',    // 其余浅色
        '#7a9e9f',
        '#7a9e9f'
      ],
      borderWidth: 0,
      borderRadius: 3
    }]
  },
  options: {
    indexAxis: 'y',                     // 水平柱状图
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        grid: { color: '#f0ece2' },
        border: { display: false },
        title: { display: true, text: '[单位]' }
      },
      y: {
        grid: { display: false },
        border: { display: false }
      }
    }
  }
});
```

### 3. 散点图（两变量关系）

```javascript
new Chart(ctx, {
  type: 'scatter',
  data: {
    datasets: [
      {
        label: '测量数据',
        data: [
          {x: 1.0, y: 2.3},
          {x: 1.5, y: 3.1},
          /* ... */
        ],
        backgroundColor: 'rgba(47,79,79,0.7)',
        pointRadius: 5,
        pointHoverRadius: 8
      },
      {
        // 拟合线（如有）
        label: '拟合曲线',
        data: [/* 拟合点 */],
        type: 'line',
        borderColor: '#c0392b',
        borderWidth: 1.5,
        borderDash: [6, 3],
        pointRadius: 0,
        fill: false
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        title: { display: true, text: '[x变量 / 单位]' },
        grid: { color: '#f0ece2' },
        border: { display: false }
      },
      y: {
        title: { display: true, text: '[y变量 / 单位]' },
        grid: { color: '#f0ece2' },
        border: { display: false }
      }
    }
  }
});
```

### 4. 误差棒折线图（均值±标准差）

Chart.js原生不支持error bar，使用以下方案：

```javascript
// 方案A：用自定义plugin绘制误差棒
const errorBarPlugin = {
  id: 'errorBar',
  afterDatasetsDraw(chart) {
    const { ctx, data, scales: {x, y} } = chart;
    data.datasets[0].errorBars?.forEach((err, i) => {
      const xPos = x.getPixelForValue(i);
      const yPos = y.getPixelForValue(data.datasets[0].data[i]);
      const errPx = Math.abs(y.getPixelForValue(err) - y.getPixelForValue(0));
      ctx.save();
      ctx.strokeStyle = '#2f4f4f';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(xPos, yPos - errPx);
      ctx.lineTo(xPos, yPos + errPx);
      // 横线
      ctx.moveTo(xPos - 6, yPos - errPx);
      ctx.lineTo(xPos + 6, yPos - errPx);
      ctx.moveTo(xPos - 6, yPos + errPx);
      ctx.lineTo(xPos + 6, yPos + errPx);
      ctx.stroke();
      ctx.restore();
    });
  }
};

// 数据结构示例：
// data.datasets[0].data = [均值数组]
// data.datasets[0].errorBars = [标准差数组]
```

---

## 多图表并排布局

```html
<!-- 两图并排 -->
<div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:16px 0;">
  <figure>
    <div class="chart-container"><canvas id="chart-a"></canvas></div>
    <figcaption>图2a. [左图描述性标题]</figcaption>
  </figure>
  <figure>
    <div class="chart-container"><canvas id="chart-b"></canvas></div>
    <figcaption>图2b. [右图描述性标题]</figcaption>
  </figure>
</div>
```

---

## 颜色使用规则

```
主色（强调最重要的数据）：    #2f4f4f  墨绿
次要色（第二重要）：          #7a9e9f  浅绿
中性色（背景/对照）：         #aab0b8  中灰
次要系列：                   #c8cdd3  浅灰
警示/异常值：                 #c0392b  深红
成功/达标：                   #27ae60  绿色

禁止使用：彩虹色、荧光色、超过4种主色
```

---

## figcaption写法规范（描述性标题）

**❌ 轴标签式（不好）：**
> 图3. 温度与反应速率

**✅ 描述性（好）：**
> 图3. 温度升高10°C时反应速率提升约2.3倍，在80°C时达到峰值并趋于稳定

描述性标题直接传达洞察，让读者无需解读图形就能了解核心发现。
