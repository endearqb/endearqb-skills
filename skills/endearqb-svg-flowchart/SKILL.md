---
name: svg-flowchart
description: |
  生成高质量的 SVG 流程图，支持垂直流程图、水平流程图、带判断分支的流程图、以及多列分组流程图。
  接受用户的文字步骤描述或列表，输出标准 SVG 文件（可直接嵌入 HTML 报告、Word 文档等）。
  
  触发条件（凡符合以下任一项，均应使用本 skill）：
  - 用户说"帮我画流程图"、"生成流程图"、"做个流程图"、"画个步骤图"
  - 用户提供了 3 个以上有序步骤并希望可视化
  - 用户说"实验步骤图"、"操作流程图"、"工艺流程图"、"工作流图"
  - 用户上传文档并要求提取步骤生成流程图
  - 任何 "流程" + "图/可视化/绘制" 的组合请求
  - 用户需要含判断/条件分支的流程图（如"合格/不合格"、"是/否"分支）
  
  输出格式：独立 `.svg` 文件，可选同时生成嵌入演示用的 HTML 预览页面。
---

# SVG Flowchart Maker — 专业流程图生成 Skill

## 概览

本 skill 将用户描述的流程步骤转换为标准化、风格统一的 SVG 流程图。
核心流程：**步骤解析 → 布局选型 → SVG 生成 → 文件输出**

---

## 第一步：信息采集与确认

### 必须收集的信息

| 信息项 | 说明 | 无则处理 |
|--------|------|---------|
| 流程步骤 | 各步骤标题（必须） | 无法继续，必须询问 |
| 步骤说明 | 每步骤的补充说明文字（可选） | 步骤框只写标题 |
| 分支条件 | 判断节点的条件描述（有分支时必须） | 菱形框内写「[条件]」占位 |
| 流程标题 | 整个流程图的标题（可选） | 省略标题区 |
| 输出用途 | 嵌入HTML报告 / 独立文件 / 其他 | 默认独立 `.svg` 文件 |

### 生成前确认（调用 ask_user_input）

信息采集完成后，**必须调用 `ask_user_input` 工具**确认以下选项：

```
问题1（single_select）：
  标题：布局方向
  选项：["垂直（从上到下）", "水平（从左到右）", "自动判断"]
  默认：自动判断

问题2（single_select）：
  标题：是否含判断分支
  选项：["是（有 是/否 或 条件 分支）", "否（线性步骤）", "自动判断"]
  默认：自动判断

问题3（single_select）：
  标题：配色风格
  选项：["暖墨纸（默认）", "清爽蓝绿", "极简灰白", "工程橙"]
  默认：暖墨纸

问题4（single_select）：
  标题：附加输出
  选项：["仅 SVG 文件", "SVG + HTML 预览页"]
  默认：仅 SVG 文件
```

根据回答设定工作变量：

| 变量 | 值 |
|------|----|
| `LAYOUT` | `vertical` / `horizontal` / `auto` |
| `HAS_BRANCH` | `true` / `false` |
| `THEME` | `default` / `blue` / `minimal` / `engineering` |
| `NEED_HTML` | `true` / `false` |

---

## 第二步：布局自动判断（当 LAYOUT=auto 时）

```
步骤数 ≤ 4 且无分支  →  水平布局
步骤数 5–8 且无分支  →  垂直布局
步骤数 > 8 且无分支  →  垂直分组（每组 4 步，多列）
含分支               →  垂直 + 菱形判断节点
```

---

## 第三步：SVG 生成规范

读取 `references/svg-spec.md` 获取：
- 箭头 marker 标准写法（`orient="auto"` 机制）
- 各布局的坐标计算公式
- 节点类型（矩形步骤框 / 菱形判断 / 圆角开始结束 / 平行四边形输入输出）
- 配色方案（4 套主题）

### 核心生成规则（摘要）

**SVG 根元素（必须）**：
```xml
<svg width="100%" viewBox="0 0 680 {H}" xmlns="http://www.w3.org/2000/svg">
```
- `viewBox` 宽度固定 680，高度 H 按内容推导（公式见 svg-spec.md）
- **不写死 `width` 像素值**，`width="100%"` 保证响应式

**箭头必须遵守**：
```xml
<marker id="arr" markerWidth="10" markerHeight="7"
        refX="9" refY="3.5" orient="auto">
  <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
  <!-- 尖端在 x 最大处 (10,3.5) → orient="auto" 时自动朝向连线终点 -->
</marker>
```

**步骤框标准尺寸**（基于 viewBox 680）：
- 宽：260px（垂直）/ 自适应（水平，按公式压缩）
- 高：44px（单行）/ 64px（双行标题+说明）/ 72px（长标题两行）
- 圆角：`rx="8"`（统一，不用 rx=12/14）
- 步骤间箭头区：28px
- 开始/结束胶囊：160×32，`rx="16"`

**文字必须用 dominant-baseline**：
```xml
<!-- 正确：y = 节点垂直中心，dominant-baseline 保证视觉居中 -->
<text x="340" y="{node_top + node_height/2}"
      text-anchor="middle" dominant-baseline="central"
      font-size="14" font-family="Georgia,serif" fill="#1d2328">标题</text>
```
- 标题：`font-size="14"` + `dominant-baseline="central"`
- 说明：`font-size="12"` + `dominant-baseline="central"`，y = 标题 y + 22
- 条件标注：偏移 10px 避免压线，不放箭头正中心

**viewBox 高度快速估算**（精确公式见 svg-spec.md）：
- 垂直 N 步（双行节点）：`H ≈ 172 + N×92`
- 水平（双行节点）：`H = 164`（固定）
- 含分支：按各区域累加

---

## 第四步：文件输出

### 输出路径

```bash
# SVG 文件
outputs/flowchart.svg

# HTML 预览页（NEED_HTML=true 时）
outputs/flowchart-preview.html
```

### HTML 预览页结构（当 NEED_HTML=true）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>流程图预览</title>
  <style>
    body { background: #f5f2ea; display: flex; flex-direction: column;
           align-items: center; padding: 2rem; font-family: Arial, sans-serif; }
    h1 { font-size: 1.1rem; color: #555; margin-bottom: 1rem; }
    .svg-wrapper { background: #fff; border-radius: 12px;
                   box-shadow: 0 2px 12px rgba(0,0,0,.1); padding: 2rem; }
    svg { max-width: 100%; height: auto; display: block; }
  </style>
</head>
<body>
  <h1>流程图预览</h1>
  <div class="svg-wrapper">
    <!-- 将 flowchart.svg 的内容直接粘贴在此 -->
  </div>
</body>
</html>
```


---

## 执行检查清单

- [ ] 已调用 `ask_user_input` 确认布局方向、分支、配色、附加输出
- [ ] 已读取 `references/svg-spec.md` 获取箭头机制和坐标公式
- [ ] 箭头 marker path 尖端在 x 最大处（`orient="auto"` 方向正确）
- [ ] `refY = markerHeight / 2`，箭头不偏离连线
- [ ] 所有步骤框尺寸统一，文字居中
- [ ] 超过 12 字的标题已拆成两行
- [ ] viewBox 尺寸已按步骤数计算，无裁剪
- [ ] SVG 文件已保存到 `outputs/flowchart.svg`
- [ ] 已调用 `present_files` 向用户提供文件

---

## 参考文件索引

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/svg-spec.md` | 完整 SVG 规范：箭头机制、坐标公式、4套主题配色、3种布局模板代码 | **生成 SVG 前必读** |
