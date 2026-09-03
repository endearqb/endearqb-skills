# 页面结构与布局系统

> Skill 路径：`product-story-pptx/references/layout-system.md`

布局不是把元素摆满，而是为当前页面决定：**观众先看什么、第二看什么、哪里停一下。**

本系统采用固定画布、有限页面类型和明确文字预算，以约束换取稳定质量。

## 1. 画布与安全区

- 比例：16:9。
- 尺寸：13.333 × 7.5 英寸。
- 左右安全边距：0.8 英寸。
- 上下安全边距：约 0.6–0.7 英寸。
- 页脚基线：距顶部 7.0 英寸。
- 所有坐标来源：`assets/layout-registry.yaml`。

图片允许越过安全区形成 bleed；文字不允许越界。

## 2. 隐含 12 栏网格

Registry 直接保存最终坐标，但布局思考按 12 栏进行：

- 12 栏：全宽内容。
- 7/5 或 6/6：文字与图片。
- 4/4/4：三个并列步骤或证据。
- 3/3/3/3：四个轻量功能点。

同一页最多两个主要左对齐轴。不要出现标题对齐一条线、正文另一条线、卡片又一条线的“漂浮边缘”。

## 3. 视觉层级

每页最多三级：

1. Action title。
2. 主视觉或核心证据。
3. 注释、来源、页脚。

出现第四、第五级时，观众必须自行判断顺序，页面会失去演示性。

### 一页一事

一页应该完成一个动作：

- 承诺。
- 建立问题。
- 解释机制。
- 展示功能。
- 提供证据。
- 对照新旧。
- 发出行动。

不要同时“讲市场、讲技术、讲案例”。

## 4. 页面类型库

| Type | 核心任务 | 主要字段 | 推荐内容量 | 允许 bleed |
|---|---|---|---|---|
| `cover` | 承诺、定调 | label/title/body/image | 极低 | full/overlay/color-block/half/half-top/edge |
| `section` | 翻篇、概念转折 | label/title | 极低 | color-block/full/partial-left/none |
| `statement` | 建立张力或换气 | title/body | 低 | none/color-block/full |
| `quote` | 人的证据与共鸣 | quote/attribution/title | 低 | none/partial/half-top/half-bottom |
| `feature_hero` | 展示关键能力与体验 | label/title/body 或 bullets/image/ui_mockup | 中低 | half/half-top/half-bottom/partial/edge/full |
| `split` | 两类信息并列 | title/body 或 bullets/image/ui_mockup | 中 | half/half-top/half-bottom/partial/none |
| `bullets` | 解释少量原则或收益 | title/bullets | 中 | none/edge |
| `compare` | 新旧、前后或方案对照 | title/left/right | 中 | none |
| `flow` | 解释顺序、机制、层级 | title/steps | 中 | none/color-block |
| `chart` | 用数据证明一个结论 | title/chart | 中 | none |
| `big_number` | 形成一个记忆锚点 | number/title/caption/source | 低 | none/color-block/partial-right |
| `gallery` | 多视角产品或场景 | title/images | 低 | none |
| `media_bars` | 条目与专属图片一一对应 | title/items/bar_width_ratio | 中 | none |
| `closing` | 新常态与 CTA | title/body/image | 极低 | full/overlay/color-block |

## 5. Type 选择决策

### 只有一句强主张

- 想制造停顿：`statement`。
- 是章节翻篇：`section`。
- 是结尾行动：`closing`。

### 有一张关键图或截图

- 图片承担一半信息：`feature_hero + half/partial`。
- 图片只是产品特写：`feature_hero + edge`。
- 图片本身就是情绪：`feature_hero/cover/closing + full`。

### 有 3–7 个步骤

- 有明确顺序：`flow`。
- 只是并列能力：不要伪装成流程，用 `bullets` 或拆成 feature hero。

### 有数字

- 一个数字且需要记忆：`big_number`。
- 类别比较：`chart: bar/hbar`。
- 时间趋势：`chart: line`。
- 两个时间点变化：`chart: slope`。
- 排名/精确位置：`chart: dot`。

### 有前后状态

- 两侧都是短列表：`compare`。
- 需要真实画面：两页 feature hero，比一页塞两张截图更清楚。

### 有 3–5 个并列条目，且每条都有专属图片

- 使用 `media_bars`，不要把 3–5 张图挤成普通 gallery。
- `bar_width_ratio` 默认 `0.60`；只决定文字条宽度，剩余空间留给配图。
- `media_side: alternating` 让配图左右交错；一条只对应一张图，图片内容必须与该条目语义一致。
- 最多一个 highlight，避免每个 bar 都抢注意力。

## 6. 文字预算

### 全局上限

- Action title：中文 ≤ 24 字；英文 ≤ 14 词。
- 正文：中文 ≤ 60 字；英文 ≤ 40 词。
- Bullets：≤ 4 条。
- 每条 bullet：中文 ≤ 20 字；英文 ≤ 12 词。
- 压图页 title + body：中文 ≤ 24 字；英文 ≤ 12 词。
- 流程 label：中文 ≤ 6 字；英文 ≤ 3 词。

### 内容密度原则

如果需要把字体缩到 14pt 才放得下，内容结构已经失败。依次考虑：

1. 删除重复解释。
2. 把名词短语改成动作句。
3. 拆页。
4. 改为图表、流程或对照。
5. 最后才微调字号。

## 7. 留白

非 full bleed 页面至少约 30% 空间不承担显性信息。

留白不是“没做完”，它完成三件事：

- 建立层级。
- 给讲者留下解释空间。
- 让相邻高能量页面形成反差。

典型错误是看到空白就补图标、补小卡、补背景线。不要填满。

## 8. 页面节奏

### 重复控制

- 相邻两页不应完全相同的 `type + bleed`。
- 同一 type 最多连续两页。
- Feature hero 可连续两页，但左右方向必须变化。
- 连续两页图表后必须换气。
- 每一幕开头应通过 section、full 或 color-block 形成视觉断点。

### 视觉重量交替

```text
文字安静页 → 图片 hero → 结构解释 → 数据证据 → 人的证据 → 视觉峰值
```

不要连续：

```text
截图 → 截图 → 截图
卡片网格 → 卡片网格 → 卡片网格
柱状图 → 折线图 → 表格
```

## 9. 标题带与内容区

`chart`、`flow`、`compare`、`gallery` 使用固定标题带：

- Kicker 可选。
- Action title 位于左上。
- 主内容从标题下方约 0.25 英寸开始。
- 来源位于主内容内部底部或页面页脚上方。

这样可以在翻页时维持阅读起点一致，内容变化不会造成页面跳动。

## 10. 页脚

- Cover、section、closing 默认隐藏页脚。
- 普通页面显示产品/项目名与页码。
- 页码两位数字，例如 `03 / 12`。
- Partial-left 页面，页脚标签移到文字列，避免落在浅色图片上。
- 页脚不能成为第三个品牌标识，不使用大 logo。

## 11. 对照页

`compare` 的重点不是“两张一样的卡”，而是方向性：

- 左侧旧状态：低对比、灰色。
- 右侧新状态：强调色、清晰动作。
- 两侧条目数量尽量一致。
- 文案长度差异不超过约 1.5 倍。
- 如果每侧超过 4 条，提炼为 3 个机制差异，详细项移附录。

## 12. Gallery

- 2–4 张图。
- 同一裁切比例和视觉距离。
- 不同时混用实拍、截图、线稿和 3D 渲染。
- Gallery 只负责展示，不在每张图上再放标题卡。
- 需要解释时，拆成多页 feature hero。
- 需要保留统一结论或证据口径时，可在图片组下方增加一行 `caption` 与一行 `source`；不要为每张图分别堆文字。

## 13. 视觉单元上限

一页最多 5 个视觉单元。一个单元可以是：

- 一张图片。
- 一个数字。
- 一个流程节点。
- 一组被视觉上合并的柱子。
- 一块对照区域。

流程图有 7 个节点是规则例外，因为它们被一个统一结构包裹；但节点内部仍应极简。

## 14. 常见崩坏

### “每页都有卡片”

卡片是 UI 容器，不是演示文稿的默认语言。大量卡片会让产品 deck 看起来像 dashboard 截图。

### 标题居中、正文左对齐、图又右对齐

三个视觉轴彼此竞争。优先整体左对齐，只有 section、数字峰值或极简 closing 才考虑居中。

### 装饰性图标网格

如果四个图标拿掉后信息不变，图标只是噪音。用编号、关键词和留白更有力量。

### 强调线滥用

每页都有一根彩色短线，会从 motif 退化为模板痕迹。只在 section 或对照边界使用。

## 15. QA

- 页面缩到 25% 时，第一视觉焦点是否仍明确？
- 标题、图与来源是否形成一个稳定阅读路径？
- 是否存在为了填空而添加的元素？
- 同类页面是否保持一致，但相邻页面又有足够变化？
- 文字是否能在 5–8 米投影距离阅读？
- 只看缩略图，三幕和章节断点是否可见？
- Media bars 是否做到条目与图片一一对应，而不是复用无关装饰图？
