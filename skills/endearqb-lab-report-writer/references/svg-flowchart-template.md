# SVG流程图模板与规范

## 触发条件

**仅在以下情况绘制SVG流程图：**
- 用户描述了实验步骤或操作流程（≥ 3个步骤）
- 用户明确要求画流程图
- 实验涉及复杂的多阶段工序

**不绘制的情况：**
- 用户只有文字描述但没有明确步骤
- 用户没有提供流程信息

---

## ⚠️ 箭头方向核心机制（必读，不可忽略）

### `orient="auto"` 的工作原理

SVG `<marker>` 的 `orient="auto"` 会将 marker 的**本地 +x 轴**旋转对齐到连线的行进方向。

**关键推论：箭头尖必须指向 marker 本地坐标的 +x 方向**（即 path 中 x 坐标最大的顶点为尖端）。

```
正确 ✅：尖端在 +x 方向（x 最大处）
  <path d="M0,0 L0,6 L9,3 z"/>
  解释：顶点分别在 (0,0)、(0,6)、(9,3)
        x 最大的顶点是 (9,3) → 箭头尖在此 → 指向 +x → 朝向连线终点 ✓

错误 ❌：尖端在 -x 方向（x 最小处）
  <path d="M9,0 L9,6 L0,3 z"/>
  解释：x 最小的顶点是 (0,3) → 箭头尖在此 → 指向 -x → 箭头反向 ✗
```

### 配套 `refX` 设置

`refX` 决定 marker 的哪个点对齐到连线终点：
- **`refX="9"`（推荐）**：将箭头尖（x=9 处）对齐到终点，箭头不超出节点边缘
- **`refX="8"`**：箭头尖略微缩入连线内（适合线段末端有间距时）

```xml
<!-- 标准箭头 marker 写法 -->
<marker id="arr" markerWidth="10" markerHeight="7"
        refX="9" refY="3.5" orient="auto">
  <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
</marker>
```

### 常见错误排查

| 症状 | 原因 | 修复方法 |
|------|------|---------|
| 箭头反向（指向起点） | path 尖端在 x 最小处 | 翻转 path，确保 x 最大顶点为尖端 |
| 箭头偏离连线 | `refY` 不等于箭头高度的一半 | 设 `refY = markerHeight / 2` |
| 箭头悬空不贴终点 | `refX` 过小 | 将 `refX` 设为箭头尖的 x 坐标值 |
| 水平箭头正常，垂直反向 | `orient` 未设为 `"auto"` | 检查 `orient="auto"` 是否存在 |

---

## 配色规范（与HTML报告一致）

```
步骤框背景色：
  #f4f1e8  暖白（通用步骤）
  #eef3f0  淡绿（关键步骤/成功路径）
  #f0f2f6  淡蓝（数据采集步骤）
  #fdf4f4  淡红（注意/风险步骤）

边框色：   #283239（深墨色）
箭头色：   #2f4f4f（墨绿）
文字色：   #1d2328（主文字）
副文字色： #5c6570（说明文字）
字体：     Georgia serif（标题）/ Arial sans-serif（说明）
```

---

## 垂直流程图模板（4步）

适合：线性实验流程

```svg
<svg width="560" height="316" viewBox="0 0 560 316" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
    </marker>
  </defs>

  <!-- 步骤1：节点垂直中心 y=48（20+56/2） -->
  <rect x="160" y="20" width="240" height="56" rx="8" fill="#f4f1e8" stroke="#283239" stroke-width="1.5"/>
  <text x="280" y="38" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="#1d2328">[步骤1标题]</text>
  <text x="280" y="58" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明文字]</text>

  <!-- 箭头1→2 -->
  <line x1="280" y1="76" x2="280" y2="100" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤2：节点垂直中心 y=128（100+56/2） -->
  <rect x="160" y="100" width="240" height="56" rx="8" fill="#eef3f0" stroke="#283239" stroke-width="1.5"/>
  <text x="280" y="118" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="#1d2328">[步骤2标题]</text>
  <text x="280" y="138" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明文字]</text>

  <!-- 箭头2→3 -->
  <line x1="280" y1="156" x2="280" y2="180" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤3：节点垂直中心 y=208（180+56/2） -->
  <rect x="160" y="180" width="240" height="56" rx="8" fill="#f0f2f6" stroke="#283239" stroke-width="1.5"/>
  <text x="280" y="198" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="#1d2328">[步骤3标题]</text>
  <text x="280" y="218" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明文字]</text>

  <!-- 箭头3→4 -->
  <line x1="280" y1="236" x2="280" y2="260" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤4：节点垂直中心 y=288（260+56/2） -->
  <rect x="160" y="260" width="240" height="56" rx="8" fill="#f4f1e8" stroke="#283239" stroke-width="1.5"/>
  <text x="280" y="278" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="#1d2328">[步骤4标题]</text>
  <text x="280" y="298" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明文字]</text>
</svg>
```

---

## 水平流程图模板（3步）

适合：简单线性流程，横向展示

```svg
<svg width="880" height="160" viewBox="0 0 880 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-h" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
    </marker>
  </defs>

  <!-- 步骤1：节点垂直中心 y=80（40+80/2） -->
  <rect x="30" y="40" width="220" height="80" rx="8" fill="#f4f1e8" stroke="#283239" stroke-width="1.5"/>
  <text x="140" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="#1d2328">[步骤1]</text>
  <text x="140" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明]</text>

  <!-- 箭头 -->
  <line x1="250" y1="80" x2="330" y2="80" stroke="#2f4f4f" stroke-width="2.5" marker-end="url(#arr-h)"/>
  <text x="290" y="68" text-anchor="middle" font-size="11" font-family="Arial,sans-serif" fill="#2f4f4f">[条件]</text>

  <!-- 步骤2：节点垂直中心 y=80（40+80/2） -->
  <rect x="330" y="40" width="220" height="80" rx="8" fill="#eef3f0" stroke="#283239" stroke-width="1.5"/>
  <text x="440" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="#1d2328">[步骤2]</text>
  <text x="440" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明]</text>

  <!-- 箭头 -->
  <line x1="550" y1="80" x2="630" y2="80" stroke="#2f4f4f" stroke-width="2.5" marker-end="url(#arr-h)"/>

  <!-- 步骤3：节点垂直中心 y=80（40+80/2） -->
  <rect x="630" y="40" width="220" height="80" rx="8" fill="#f0f2f6" stroke="#283239" stroke-width="1.5"/>
  <text x="740" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="#1d2328">[步骤3]</text>
  <text x="740" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#5c6570">[说明]</text>
</svg>
```

---

## 带判断分支的流程图模板

适合：含条件判断的实验流程（如：合格/不合格分支）

```svg
<svg width="600" height="460" viewBox="0 0 600 460" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-b" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
    </marker>
  </defs>

  <!-- 开始：节点垂直中心 y=45（20+50/2） -->
  <rect x="200" y="20" width="200" height="50" rx="25" fill="#2f4f4f" stroke="none"/>
  <text x="300" y="45" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="#fff">开始</text>

  <line x1="300" y1="70" x2="300" y2="110" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr-b)"/>

  <!-- 步骤框：节点垂直中心 y=137.5（110+55/2） -->
  <rect x="180" y="110" width="240" height="55" rx="8" fill="#f4f1e8" stroke="#283239" stroke-width="1.5"/>
  <text x="300" y="137" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="#1d2328">[操作步骤]</text>

  <line x1="300" y1="165" x2="300" y2="205" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr-b)"/>

  <!-- 判断菱形 -->
  <polygon points="300,205 400,255 300,305 200,255" fill="#fff9e6" stroke="#c9a227" stroke-width="1.5"/>
  <text x="300" y="255" text-anchor="middle" dominant-baseline="central" font-size="13" font-family="Arial,sans-serif" fill="#1d2328">[判断条件]？</text>

  <!-- 是→右 -->
  <line x1="400" y1="255" x2="480" y2="255" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr-b)"/>
  <text x="440" y="245" text-anchor="middle" font-size="12" fill="#2f4f4f">是</text>
  <rect x="480" y="225" width="100" height="60" rx="8" fill="#eef3f0" stroke="#283239" stroke-width="1.5"/>
  <text x="530" y="255" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="#1d2328">[处理A]</text>

  <!-- 否→下 -->
  <line x1="300" y1="305" x2="300" y2="345" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr-b)"/>
  <text x="316" y="330" font-size="12" fill="#2f4f4f">否</text>
  <rect x="180" y="345" width="240" height="55" rx="8" fill="#fdf4f4" stroke="#c0392b" stroke-width="1.5"/>
  <text x="300" y="372" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="#1d2328">[处理B / 重做]</text>

  <!-- 结束：节点垂直中心 y=435（420+30/2） -->
  <line x1="300" y1="400" x2="300" y2="420" stroke="#2f4f4f" stroke-width="2" marker-end="url(#arr-b)"/>
  <rect x="200" y="420" width="200" height="30" rx="15" fill="#1f2328" stroke="none"/>
  <text x="300" y="435" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="#fff">结束</text>
</svg>
```

---

## 步骤框间距计算

每个步骤框高度 56px，步骤框间距 24px（箭头区域），顶部和底部各留 20px，则：

```
垂直 N 步流程图总高 H = 20 + N×56 + (N-1)×24 + 20
                      = N×80 − 4
```

| N | 高度 H |
|---|--------|
| 2 | 156 |
| 3 | 236 |
| 4 | 316 |
| 5 | 396 |
| 6 | 476 |
| 7 | 556 |

> ⚠️ 旧写法 `N×80+20` 漏掉底部留白，末节点底边会贴住 viewBox 边缘，stroke 可能被裁切。务必用新公式。

---

## 步骤数量适配

| 步骤数 | 建议布局 | SVG尺寸参考 |
|--------|----------|------------|
| 2–4步 | 垂直或水平 | `560 × (N×80−4)` 或 880×160 |
| 5–7步 | 垂直 | `560 × (N×80−4)` |
| 8步以上 | 分组水平+垂直混合，或拆成多个子流程图 | — |
| 含分支 | 带菱形判断节点 | 按内容手动测量 |
