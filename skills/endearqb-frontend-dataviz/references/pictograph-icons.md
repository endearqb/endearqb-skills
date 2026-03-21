# 拟物图表 SVG 图标库

使用方式：将 SVG 内嵌到 HTML，用 JS 转为 canvas pattern 填充条形图。
颜色占位符用 `[COLOR]` 替代，运行时动态替换。

---

## 食品类

### 薯条
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <rect x="3" y="8" width="3" height="14" rx="1"/>
  <rect x="7" y="5" width="3" height="17" rx="1"/>
  <rect x="11" y="6" width="3" height="16" rx="1"/>
  <rect x="15" y="8" width="3" height="14" rx="1"/>
  <rect x="19" y="7" width="3" height="15" rx="1"/>
  <rect x="2" y="20" width="20" height="3" rx="1" fill="#C0392B"/>
</svg>
```

### 咖啡杯
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <path d="M4 6h13v10a4 4 0 01-4 4H8a4 4 0 01-4-4V6z"/>
  <path d="M17 8h1a3 3 0 010 6h-1" fill="none" stroke="[COLOR]" stroke-width="2"/>
</svg>
```

### 披萨
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <path d="M12 2L2 19h20L12 2z"/>
  <circle cx="12" cy="12" r="1.5" fill="white"/>
  <circle cx="9" cy="15" r="1" fill="white"/>
  <circle cx="15" cy="14" r="1" fill="white"/>
</svg>
```

---

## 人员类

### 人形图标
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <circle cx="12" cy="5" r="3"/>
  <path d="M6 20v-4a6 6 0 0112 0v4"/>
</svg>
```

### 团队（多人）
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <circle cx="9" cy="5" r="2.5"/>
  <circle cx="15" cy="5" r="2.5"/>
  <path d="M3 19v-3a5 5 0 0110 0v3"/>
  <path d="M11 19v-3a5 5 0 0110 0v3"/>
</svg>
```

---

## 交通类

### 汽车
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <path d="M5 11l1.5-4.5h11L19 11"/>
  <rect x="2" y="11" width="20" height="6" rx="2"/>
  <circle cx="7" cy="19" r="2"/>
  <circle cx="17" cy="19" r="2"/>
</svg>
```

### 飞机
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 00-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
</svg>
```

---

## 自然类

### 树木
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <polygon points="12,2 4,14 20,14"/>
  <polygon points="12,7 5,17 19,17"/>
  <rect x="10" y="17" width="4" height="5"/>
</svg>
```

### 水滴
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <path d="M12 2C12 2 4 10 4 15a8 8 0 0016 0C20 10 12 2 12 2z"/>
</svg>
```

---

## 科技类

### 电池（电量/能耗）
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <rect x="2" y="7" width="18" height="10" rx="2"/>
  <rect x="20" y="10" width="2" height="4" rx="1"/>
  <rect x="4" y="9" width="10" height="6" rx="1" fill="white" opacity="0.8"/>
</svg>
```

### 星形评分
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="[COLOR]">
  <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
</svg>
```

---

## 实现代码模板

```javascript
// 创建图标 pattern 用于 Chart.js 条形图填充
async function createIconPattern(svgTemplate, color, size = 28) {
  const svgStr = svgTemplate.replace(/\[COLOR\]/g, color);
  const blob = new Blob([svgStr], {type: 'image/svg+xml'});
  const url = URL.createObjectURL(blob);
  
  return new Promise(resolve => {
    const img = new Image(size, size);
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = size; canvas.height = size + 4;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 2, size, size);
      URL.revokeObjectURL(url);
      resolve(ctx.createPattern(canvas, 'repeat-y'));
    };
    img.src = url;
  });
}

// 使用示例
const pattern = await createIconPattern(FRIES_SVG, '#F59E0B');
chart.data.datasets[0].backgroundColor = pattern;
chart.update();
```

**注意**：拟物图表适合展示性/演示场合，精确数值读取能力低于普通条形图。
建议同时显示数值标签补充。
