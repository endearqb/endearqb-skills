# SVG 流程图完整规范

## 目录
1. [SVG 根元素与 viewBox 最佳实践](#svg-根元素与-viewbox-最佳实践)
2. [箭头核心机制](#箭头核心机制)
3. [节点尺寸与文字纵向排列](#节点尺寸与文字纵向排列)
4. [配色主题](#配色主题)
5. [坐标计算公式（内容自适应）](#坐标计算公式内容自适应)
6. [布局模板：垂直流程图](#垂直流程图模板)
7. [布局模板：水平流程图](#水平流程图模板)
8. [布局模板：带判断分支](#带判断分支模板)
9. [步骤数量适配规则](#步骤数量适配规则)

---

## SVG 根元素与 viewBox 最佳实践

### 黄金规则：width="100%" + 固定 viewBox

```xml
<svg width="100%" viewBox="0 0 680 {H}" xmlns="http://www.w3.org/2000/svg">
```

- **`width="100%"`**：让 SVG 自适应容器宽度，不写死像素值
- **`viewBox` 宽度固定为 680**：这是与渲染容器 1:1 的坐标系，所有坐标计算基于此
- **`viewBox` 高度 H = 内容最低点 + 40px 底部缓冲**（不猜测，按公式算）
- **不设 `height` 属性**：SVG 高度由 viewBox 宽高比和容器宽度自动推导，避免裁剪

```
❌ 错误写法：<svg width="560" height="380">   → 写死像素，小屏溢出
✅ 正确写法：<svg width="100%" viewBox="0 0 680 380">   → 响应式
```

### viewBox 高度最终校验清单

生成 SVG 后，在确定 H 之前必须检查：

1. 找到所有 `<rect>` 的 `y + height` 最大值
2. 找到所有独立 `<text>` 的 `y` 最大值（基线位置 + 约 4px 字体下沿）
3. H = 以上最大值 + 40
4. 确认没有元素的 x 坐标超出 `[0, 680]` 范围

### 内容安全区

```
左右留白：x ∈ [40, 640]（两侧各 40px）
上下留白：y ∈ [40, H-40]
流程图内容中心：x = 340（680 / 2）
```

---

## 箭头核心机制

### `orient="auto"` 工作原理

SVG `<marker>` 的 `orient="auto"` 会将 marker 的**本地 +x 轴**旋转对齐到连线的行进方向。

**关键规则：箭头尖必须指向 marker 本地坐标的 +x 方向（即 path 中 x 坐标最大的顶点为尖端）。**

```
正确 ✅：尖端在 +x 方向（x 最大处）
  <path d="M0,0 L0,6 L9,3 z"/>
  顶点：(0,0)、(0,6)、(9,3) → x 最大在 (9,3) → 箭头尖朝 +x → 指向连线终点 ✓

错误 ❌：尖端在 -x 方向（x 最小处）
  <path d="M9,0 L9,6 L0,3 z"/>
  顶点：x 最小在 (0,3) → 箭头反向 ✗
```

### 标准箭头 Marker 定义

```xml
<defs>
  <marker id="arr" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
  </marker>
</defs>
```

- `refX="9"`：将箭头尖（x=9 处）对齐到连线终点，不超出节点边缘
- `refY="3.5"`：等于 `markerHeight / 2 = 3.5`，箭头垂直居中于连线
- 箭头使用：`<line ... marker-end="url(#arr)"/>`

### 箭头与节点边缘的间距

**连线必须在节点边缘留 8px 缝隙**，避免箭头刺入节点内部：

```
垂直布局：
  line y1 = 节点底边 y_bot          （从底边出发，无缝隙）
  line y2 = 下一节点顶边 y_top - 0  （marker refX 已将尖端对齐到终点）
  → 但若箭头超出节点，在 y1 上加 +2，y2 处 marker 本身负责对齐

水平布局：
  line x1 = 节点右边 x_right        （从右边出发）
  line x2 = 下一节点左边 x_left     （marker 对齐）
```

**实测可靠写法**（以垂直为例）：
```xml
<line x1="340" y1="{node_bottom}" x2="340" y2="{next_top}"
      stroke="#2f4f4f" stroke-width="1.5" marker-end="url(#arr)"/>
```
`marker-end` + `refX="9"` 已自动处理终点对齐，无需手动缩短 y2。

### 常见错误排查

| 症状 | 原因 | 修复 |
|------|------|------|
| 箭头反向（指向起点） | path 尖端在 x 最小处 | 翻转 path，确保 x 最大顶点为尖端 |
| 箭头偏离连线 | `refY ≠ markerHeight / 2` | 设 `refY = 3.5`（markerHeight=7 时） |
| 箭头悬空不贴终点 | `refX` 过小 | 将 `refX` 设为箭头尖的 x 坐标（这里是 9） |
| 水平正常、垂直反向 | `orient` 未设为 `"auto"` | 检查 `orient="auto"` 是否存在 |

---

## 节点尺寸与文字纵向排列

### 节点类型与尺寸

| 类型 | SVG 元素 | 尺寸（垂直布局） | 尺寸（水平布局） |
|------|---------|--------------|--------------|
| 步骤框（单行） | `<rect rx="8">` | 240 × 44 | 220 × 44 |
| 步骤框（双行） | `<rect rx="8">` | 240 × 64 | 220 × 64 |
| 开始/结束胶囊 | `<rect rx="16">` | 180 × 32 | 180 × 32 |
| 判断菱形 | `<polygon>` | dx=110, dy=48 | dx=90, dy=44 |

**rx 规则：**
- 步骤框 `rx="8"`（subtle，与 HTML 报告卡片风格一致）
- 开始/结束用 `rx = height/2` 使之成为胶囊型（`rx="16"` 配 `height=32`）
- 判断菱形不设 rx，polygon 本身即菱形

### 文字纵向居中：必须使用 dominant-baseline

**SVG `<text>` 的 `y` 坐标默认是基线（baseline），而非视觉中心。**
不加 `dominant-baseline="central"` 时，文字会偏上约 4–6px，在小节点里视觉失衡。

```xml
<!-- ❌ 错误：凭经验偏移，在不同字体/渲染引擎下不一致 -->
<text x="340" y="{node_top + 30}">标题</text>

<!-- ✅ 正确：y = 节点垂直中心，dominant-baseline 保证视觉居中 -->
<text x="340" y="{node_top + node_height/2}"
      text-anchor="middle" dominant-baseline="central">标题</text>
```

### 单行节点的文字位置

```
节点：rect x=220, y=100, width=240, height=44
文字中心 x = 220 + 240/2 = 340
文字中心 y = 100 + 44/2  = 122

→ <text x="340" y="122" text-anchor="middle" dominant-baseline="central">步骤标题</text>
```

### 双行节点（标题 + 说明）的文字排列

双行节点高度 64px，两行文字按以下规则分布：

```
节点：rect x=220, y=100, width=240, height=64
节点垂直中心 = 100 + 32 = 132

标题行 y = 节点中心 - 行间距/2 = 132 - 11 = 121
说明行 y = 节点中心 + 行间距/2 = 132 + 11 = 143
行间距 = 22px（14px字体 + 8px间距）
```

```xml
<!-- 双行节点示例 -->
<rect x="220" y="100" width="240" height="64" rx="8"
      fill="#f4f1e8" stroke="#283239" stroke-width="0.8"/>
<text x="340" y="121" text-anchor="middle" dominant-baseline="central"
      font-size="14" font-family="Georgia,serif" fill="#1d2328">步骤标题</text>
<text x="340" y="143" text-anchor="middle" dominant-baseline="central"
      font-size="12" font-family="Arial,sans-serif" fill="#5c6570">说明文字（≤12字）</text>
```

### 箭头旁的条件标注

条件文字（"是"/"否"/"条件"）**不放在箭头正中**，而是偏移 8px 避免与连线重叠：

```
垂直箭头的条件标注：
  文字 x = 箭头 x1 + 10（向右偏移，避免压线）
  文字 y = 箭头中点 y

水平箭头的条件标注：
  文字 x = 箭头中点 x
  文字 y = 箭头 y1 - 10（向上偏移，避免压线）
```

```xml
<!-- 水平箭头上方的条件文字 -->
<text x="{(x1+x2)/2}" y="{arrow_y - 10}"
      text-anchor="middle" dominant-baseline="central"
      font-size="11" font-family="Arial,sans-serif" fill="#2f4f4f">条件文字</text>
<line x1="{x1}" y1="{arrow_y}" x2="{x2}" y2="{arrow_y}"
      stroke="#2f4f4f" stroke-width="1.5" marker-end="url(#arr)"/>
```

### 长标题换行规则

当标题字符数 > 10（中文约 5 个字，英文约 10 字符）时，使用 `<tspan>` 换行，并相应增加节点高度：

```xml
<!-- 长标题两行（节点高度调整为 72px） -->
<rect x="220" y="100" width="240" height="72" rx="8" .../>
<!-- 节点中心 y = 100 + 36 = 136 -->
<text x="340" text-anchor="middle" dominant-baseline="central"
      font-size="14" font-family="Georgia,serif" fill="#1d2328">
  <tspan x="340" y="120">第一行标题文字</tspan>
  <tspan x="340" dy="20">第二行标题文字</tspan>
</text>
```

> 注意：长标题节点不再写说明行，标题本身已占两行。

---

## 配色主题

### 暖墨纸（default）

```
步骤框背景（通用）： #f4f1e8
步骤框背景（关键）： #eef3f0（淡绿）
步骤框背景（数据）： #f0f2f6（淡蓝）
步骤框背景（注意）： #fdf4f4（淡红）
判断菱形背景：      #fff9e6
边框色：            #283239
箭头色：            #2f4f4f
主文字：            #1d2328
副文字：            #5c6570
开始结束框：        #2f4f4f（背景）/ #ffffff（文字）
```

### 清爽蓝绿（blue）

```
步骤框背景（通用）： #e8f4f8
步骤框背景（关键）： #e0f0e8
步骤框背景（数据）： #dde8f5
步骤框背景（注意）： #fdeaea
判断菱形背景：      #fffbe0
边框色：            #1a4a6b
箭头色：            #1a6b5a
主文字：            #0d2233
副文字：            #3d6070
开始结束框：        #1a4a6b（背景）/ #ffffff（文字）
```

### 极简灰白（minimal）

```
步骤框背景（通用）： #fafafa
步骤框背景（关键）： #f0f0f0
步骤框背景（数据）： #f0f4f8
步骤框背景（注意）： #fff0f0
判断菱形背景：      #fffff0
边框色：            #555555
箭头色：            #444444
主文字：            #222222
副文字：            #777777
开始结束框：        #333333（背景）/ #ffffff（文字）
```

### 工程橙（engineering）

```
步骤框背景（通用）： #fff8f0
步骤框背景（关键）： #fff0e0
步骤框背景（数据）： #f0f4ff
步骤框背景（注意）： #fff0f0
判断菱形背景：      #fff8e0
边框色：            #7a3a00
箭头色：            #b85a00
主文字：            #3d1a00
副文字：            #8a5a30
开始结束框：        #b85a00（背景）/ #ffffff（文字）
```

---

## 坐标计算公式（内容自适应）

所有尺寸基于 **viewBox 宽度 = 680** 推导，确保 1:1 坐标系。

### 核心常量

```
CANVAS_W   = 680      viewBox 宽度（固定，不可更改）
CX         = 340      主干中心 x（垂直流程）
NODE_W     = 260      步骤节点宽度（垂直布局）
NODE_W_H   = 200      步骤节点宽度（水平布局）
NODE_H1    = 44       单行节点高度
NODE_H2    = 64       双行节点高度（标题+说明）
NODE_H_LONG= 72       长标题（两行标题）节点高度
PILL_W     = 160      开始/结束胶囊宽度
PILL_H     = 32       开始/结束胶囊高度（rx = 16）
GAP_V      = 28       垂直布局：节点间箭头区高度（最小值）
GAP_H      = 64       水平布局：节点间箭头区宽度（含条件文字区）
PAD_TOP    = 40       画布顶部留白
PAD_BOT    = 40       画布底部留白

节点左边 x（垂直）= CX - NODE_W/2 = 340 - 130 = 210
```

### 垂直布局高度自适应公式

每个步骤块高度 = 该步骤节点高度 + 箭头间距 GAP_V

```
定义每步块高：
  BLOCK[i] = node_height[i] + GAP_V   （最后一步不加 GAP_V）

各节点顶边 y：
  y[0]     = PAD_TOP + PILL_H + GAP_V          （开始胶囊 + 间距）
  y[i]     = y[i-1] + node_height[i-1] + GAP_V  （前一节点底边 + 间距）

画布总高度（精确）：
  content_bottom = y[N-1] + node_height[N-1] + GAP_V + PILL_H
  H = content_bottom + PAD_BOT

示例：4 步，全部双行节点（HEIGHT=64），含开始/结束胶囊：
  y[0] = 40 + 32 + 28 = 100
  y[1] = 100 + 64 + 28 = 192
  y[2] = 192 + 64 + 28 = 284
  y[3] = 284 + 64 + 28 = 376
  content_bottom = 376 + 64 + 28 + 32 = 500
  H = 500 + 40 = 540
  → <svg width="100%" viewBox="0 0 680 540">
```

### 水平布局宽高自适应公式

水平布局：viewBox 宽度固定 680，但节点数 N 会影响节点宽度。

```
可用宽度 = 680 - 2 × 40 = 600  （左右各 40px 留白）
每步总宽 = NODE_W_H + GAP_H
N 步总需宽 = N × NODE_W_H + (N-1) × GAP_H

若 N × 200 + (N-1) × 64 > 600，则压缩节点宽度：
  NODE_W_H_actual = (600 - (N-1) × 48) / N   （GAP_H 最小压缩至 48）
  若仍超出（N≥5），建议改用垂直布局

节点顶边 y（含条件文字空间）：
  condition_area = 20   （箭头上方条件文字高度预留）
  node_top_y = PAD_TOP + condition_area = 60

单行节点：H = 60 + NODE_H1 + PAD_BOT = 60 + 44 + 40 = 144
双行节点：H = 60 + NODE_H2 + PAD_BOT = 60 + 64 + 40 = 164

各节点左边 x：
  x[i] = 40 + i × (NODE_W_H + GAP_H)
  节点中心 cx[i] = x[i] + NODE_W_H / 2

箭头：
  x1 = x[i] + NODE_W_H     （当前节点右边）
  x2 = x[i+1]               （下一节点左边）
  y  = node_top_y + node_height / 2   （节点垂直中心）
条件文字：
  text_x = (x1 + x2) / 2
  text_y = y - 10            （箭头上方 10px，不压线）
```

### 含分支布局（垂直主干 + 横向分支）

```
viewBox 宽 = 680，主干 CX = 340

侧边分支空间：
  主干节点宽 = 260
  节点左边 x = CX - 130 = 210，右边 x = CX + 130 = 470
  右侧分支节点：x_left = 510，宽度 = 140（最大，受 640 安全边界限制）
  左侧分支节点：x_right = 170，宽度 = 140，x_left = 30（刚好在安全区边缘）

判断菱形：
  中心 (CX, cy)
  dx = 120，dy = 52
  polygon points = "340,{cy-52} 460,{cy} 340,{cy+52} 220,{cy}"

分支线高度分配：
  y_diamond_center = cy
  右侧分支节点垂直中心 y = cy（与菱形同高）
  右侧箭头：x1=460（菱形右顶），y1=cy → x2=510（分支节点左边），y2=cy

各区域 y 坐标累积（与垂直布局同公式）：
  y_start_pill = PAD_TOP
  y_step[i]    = 按前一元素底边 + GAP_V 递推
  y_diamond    = 前一元素底边 + GAP_V + dy（菱形中心，顶点已隐含在 dy 中）
  y_end_pill   = 否分支节点底边 + GAP_V
  H = y_end_pill + PILL_H + PAD_BOT
```

---

## 垂直流程图模板

适合：4–8 步线性流程。以 4 步双行节点为例：

```
常量：CX=340, NODE_W=260, NODE_H2=64, GAP_V=28, PILL_W=160, PILL_H=32
y_pill_start = 40
y[0] = 40 + 32 + 28 = 100
y[1] = 100 + 64 + 28 = 192
y[2] = 192 + 64 + 28 = 284
y[3] = 284 + 64 + 28 = 376
y_pill_end = 376 + 64 + 28 = 468
H = 468 + 32 + 40 = 540
```

```svg
<svg width="100%" viewBox="0 0 680 540" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="{箭头色}"/>
    </marker>
  </defs>

  <!-- 开始胶囊：中心 x=340, y_top=40, height=32, rx=16 -->
  <rect x="260" y="40" width="160" height="32" rx="16" fill="{开始结束色}" stroke="none"/>
  <text x="340" y="56" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="#ffffff">开始</text>

  <!-- 箭头：从胶囊底边 y=72 到第一步顶边 y=100 -->
  <line x1="340" y1="72" x2="340" y2="100"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 0：y_top=100, height=64, 中心 y=132 -->
  <rect x="210" y="100" width="260" height="64" rx="8"
        fill="{步骤色1}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="121" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤1标题}</text>
  <text x="340" y="143" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤1说明}</text>

  <!-- 箭头：y1=164（节点底）→ y2=192（下一节点顶） -->
  <line x1="340" y1="164" x2="340" y2="192"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 1：y_top=192, height=64, 中心 y=224 -->
  <rect x="210" y="192" width="260" height="64" rx="8"
        fill="{步骤色2}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="213" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤2标题}</text>
  <text x="340" y="235" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤2说明}</text>

  <!-- 箭头：y1=256 → y2=284 -->
  <line x1="340" y1="256" x2="340" y2="284"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 2：y_top=284, height=64, 中心 y=316 -->
  <rect x="210" y="284" width="260" height="64" rx="8"
        fill="{步骤色3}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="305" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤3标题}</text>
  <text x="340" y="327" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤3说明}</text>

  <!-- 箭头：y1=348 → y2=376 -->
  <line x1="340" y1="348" x2="340" y2="376"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 3：y_top=376, height=64, 中心 y=408 -->
  <rect x="210" y="376" width="260" height="64" rx="8"
        fill="{步骤色4}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="397" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤4标题}</text>
  <text x="340" y="419" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤4说明}</text>

  <!-- 箭头：y1=440 → y2=468 -->
  <line x1="340" y1="440" x2="340" y2="468"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 结束胶囊：y_top=468, height=32 -->
  <rect x="260" y="468" width="160" height="32" rx="16" fill="{开始结束色}" stroke="none"/>
  <text x="340" y="484" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="#ffffff">结束</text>
</svg>
```

> 增减步骤时，按公式重新推导各 y 坐标，最后更新 viewBox height。

---

## 水平流程图模板

适合：2–4 步简单流程。以 3 步双行节点为例：

```
常量：NODE_W_H=200, GAP_H=64, NODE_H2=64
PAD_LEFT = 40
条件文字高 condition_area = 20
node_top_y = 40 + 20 = 60
node_cy = 60 + 64/2 = 92

x[0] = 40,   cx[0] = 140, x_right[0] = 240
x[1] = 304,  cx[1] = 404, x_right[1] = 504
x[2] = 568,  cx[2] = 668 → 超出安全区！

→ 3步时压缩：可用宽 600, NODE_W_H_actual = (600 - 2×48) / 3 ≈ 168
  x[0]=40,  cx[0]=124, x_right[0]=208
  x[1]=256, cx[1]=340, x_right[1]=424
  x[2]=472, cx[2]=556, x_right[2]=640 ✓

H = 60 + 64 + 40 = 164
```

```svg
<svg width="100%" viewBox="0 0 680 164" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="{箭头色}"/>
    </marker>
  </defs>

  <!-- 步骤 0：x=40, y=60, width=168, height=64 -->
  <rect x="40" y="60" width="168" height="64" rx="8"
        fill="{步骤色1}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="124" y="81" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤1标题}</text>
  <text x="124" y="103" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤1说明}</text>

  <!-- 条件文字（箭头上方 10px），箭头中点 x = (208+256)/2 = 232 -->
  <text x="232" y="82" text-anchor="middle" dominant-baseline="central"
        font-size="11" font-family="Arial,sans-serif" fill="{箭头色}">{条件}</text>
  <!-- 箭头：x1=208（右边）→ x2=256（下一左边），y=92（垂直中心） -->
  <line x1="208" y1="92" x2="256" y2="92"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 1：x=256 -->
  <rect x="256" y="60" width="168" height="64" rx="8"
        fill="{步骤色2}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="81" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤2标题}</text>
  <text x="340" y="103" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤2说明}</text>

  <!-- 箭头中点 x = (424+472)/2 = 448 -->
  <text x="448" y="82" text-anchor="middle" dominant-baseline="central"
        font-size="11" font-family="Arial,sans-serif" fill="{箭头色}">{条件}</text>
  <line x1="424" y1="92" x2="472" y2="92"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤 2：x=472 -->
  <rect x="472" y="60" width="168" height="64" rx="8"
        fill="{步骤色3}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="556" y="81" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{步骤3标题}</text>
  <text x="556" y="103" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{步骤3说明}</text>
</svg>
```

---

## 带判断分支模板

含 是/否 分支。以 1步+判断+两路分支 为例：

```
y_pill_start = 40
y_step0_top  = 40 + 32 + 28 = 100
y_diamond_cy = 100 + 64 + 28 + 52 = 244  （步骤底边 164 + GAP_V 28 + dy 52）
y_branch_rect_top = y_diamond_cy - 32 = 212  （分支节点垂直中心与菱形同高）
y_no_step_top = 244 + 52 + 28 = 324   （菱形底 296 + GAP_V 28）
y_pill_end   = 324 + 64 + 28 = 416
H = 416 + 32 + 40 = 488
```

```svg
<svg width="100%" viewBox="0 0 680 488" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="{箭头色}"/>
    </marker>
  </defs>

  <!-- 开始胶囊：y_top=40 -->
  <rect x="260" y="40" width="160" height="32" rx="16" fill="{开始结束色}" stroke="none"/>
  <text x="340" y="56" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="#ffffff">开始</text>

  <line x1="340" y1="72" x2="340" y2="100"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 步骤框：y_top=100, height=64 -->
  <rect x="210" y="100" width="260" height="64" rx="8"
        fill="{步骤色}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="121" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{操作步骤}</text>
  <text x="340" y="143" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{说明}</text>

  <!-- 箭头：y1=164 → y2=192（菱形顶点 244-52=192） -->
  <line x1="340" y1="164" x2="340" y2="192"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 判断菱形：中心 (340, 244)，dx=120，dy=52 -->
  <polygon points="340,192 460,244 340,296 220,244"
           fill="{菱形色}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="244" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="{主文字}">{判断条件}？</text>

  <!-- 是 → 右侧分支（从菱形右顶 460,244 → 分支节点左边 510,244） -->
  <text x="485" y="234" text-anchor="middle" dominant-baseline="central"
        font-size="11" font-family="Arial,sans-serif" fill="{箭头色}">是</text>
  <line x1="460" y1="244" x2="510" y2="244"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 右侧分支节点：x=510, y_top=212, width=130, height=64, 中心 y=244 -->
  <rect x="510" y="212" width="130" height="64" rx="8"
        fill="{分支色A}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="575" y="233" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="{主文字}">{处理A}</text>
  <text x="575" y="255" text-anchor="middle" dominant-baseline="central"
        font-size="11" font-family="Arial,sans-serif" fill="{副文字}">{说明A}</text>

  <!-- 否 → 向下继续（从菱形底点 340,296 → 下一节点顶 340,324） -->
  <text x="353" y="314" dominant-baseline="central"
        font-size="11" font-family="Arial,sans-serif" fill="{箭头色}">否</text>
  <line x1="340" y1="296" x2="340" y2="324"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 否路径步骤：y_top=324, height=64 -->
  <rect x="210" y="324" width="260" height="64" rx="8"
        fill="{分支色B}" stroke="{边框色}" stroke-width="0.8"/>
  <text x="340" y="345" text-anchor="middle" dominant-baseline="central"
        font-size="14" font-family="Georgia,serif" fill="{主文字}">{处理B}</text>
  <text x="340" y="367" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-family="Arial,sans-serif" fill="{副文字}">{说明B}</text>

  <!-- 箭头 → 结束 -->
  <line x1="340" y1="388" x2="340" y2="416"
        stroke="{箭头色}" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 结束胶囊：y_top=416 -->
  <rect x="260" y="416" width="160" height="32" rx="16" fill="{开始结束色}" stroke="none"/>
  <text x="340" y="432" text-anchor="middle" dominant-baseline="central"
        font-size="13" font-family="Arial,sans-serif" fill="#ffffff">结束</text>
</svg>
```

---

## 步骤数量适配规则

| 步骤数 | 建议布局 | 节点类型 | viewBox 高度估算 |
|--------|---------|---------|----------------|
| 2–3 步，无分支 | 水平 | 双行 64px | 164px |
| 4–7 步，无分支 | 垂直 | 双行 64px | `N×92+72` 近似 |
| 8 步以上 | 垂直分两列 或 拆子图 | — | — |
| 含分支（任意） | 垂直主干 + 横向分支 | — | 按节点数累加 |

**N 步垂直快速估算**（所有步骤相同高度 h）：
```
H ≈ 40 + 32 + N×(h + 28) + 28 + 32 + 40
  = 172 + N×(h + 28)

单行节点(h=44)：H ≈ 172 + N×72
双行节点(h=64)：H ≈ 172 + N×92
```

### 节点宽度与最长文字的关系

在生成节点前，先估算最长标题的渲染宽度（14px 中文约 16px/字，英文约 8px/字）：

```
min_node_width = max_title_chars × 字符宽度 + 2 × 24（内边距）

例：标题"样品前处理与称量"（9字中文）
  需要宽度 = 9×16 + 48 = 192px
  → NODE_W=260 足够 ✓

例：标题"Electrochemical Impedance Spectroscopy"（38字符英文）
  需要宽度 = 38×8 + 48 = 352px
  → NODE_W=260 不够，需拆成两行或将 NODE_W 扩大至 360
  → 拆行后节点高度改为 NODE_H_LONG=72
```
