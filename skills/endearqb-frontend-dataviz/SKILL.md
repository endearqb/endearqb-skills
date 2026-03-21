---
name: frontend-dataviz
description: >
  根据用户提供的数据生成符合 Storytelling with Data（SWD）原则的可视化图表。
  触发条件：用户提供数据并要求"画图"、"生成图表"、"可视化"、"做个图"、
  "帮我展示这些数据"，或上传 CSV/Excel/表格数据并希望看到图形化呈现时，
  必须使用本 skill。即使用户只说"帮我分析这些数据"而数据适合可视化，
  也应主动使用本 skill 生成图表。
---

# Data Visualization Skill（SWD 原则）

## 核心理念

遵循 Cole Nussbaumer Knaflic 的 **Storytelling with Data** 六大原则：

1. **理解背景** — 谁是受众？他们需要做什么决策？
2. **选择合适图表** — 见下方图表选择矩阵
3. **消除杂乱** — 删除所有不传递信息的元素（网格线、3D 效果、不必要的边框）
4. **引导注意力** — 用颜色/粗细/位置突出关键信息，其余降至背景色
5. **像设计师一样思考** — 对齐、留白、层次
6. **讲述故事** — 图表标题应是洞察，而非描述（"Q3 销售额下降 18%" 而非 "Q3 销售额"）

---

## Step 1：数据分析

拿到数据后，先判断图表类型：

| 目的 | 推荐图表 |
|------|---------|
| 比较类别 | 条形图（横向更易读标签）|
| 展示趋势 | 折线图 |
| 展示构成 | 堆叠条形 / 瀑布图 |
| 展示相关性 | 散点图 |
| 展示分布 | 直方图 / 箱线图 |
| 部分与整体 | 仅当类别 ≤5 时用饼图，否则用条形 |

---

## Step 2：用 ask_user_input_v0 工具向用户提问

**必须在生成任何图表前，使用 `ask_user_input_v0` 工具一次性提出以下两个问题。**

```javascript
ask_user_input_v0({
  questions: [
    {
      question: "颜色风格？",
      type: "single_select",
      options: [
        "专业商务（极简灰+强调色）",
        "社交媒体（鲜艳多彩，高饱和）"
      ]
    },
    {
      question: "是否使用拟物图表（pictograph）？",
      type: "single_select",
      options: [
        "普通图表",
        "拟物图表（用实物图标代替条形）"
      ]
    }
  ]
})
```

---

## Step 3：生成图表（HTML + Chart.js）

输出统一使用 HTML Artifact，内嵌 Chart.js（从 cdnjs 加载）。

**颜色风格映射：**
- 专业商务 → 灰色基调 + `#2563EB` 单强调色，其余数据点全灰 `#D1D5DB`
- 社交媒体 → 高饱和多色方案，见 `references/color-palettes.md`

**拟物图表：** 用户选择后，使用 SVG Pattern + Chart.js canvas 实现，见 `references/pictograph-icons.md`

**SWD 视觉规范（必须遵守）：**
```
网格线：极浅灰 #F3F4F6 或隐藏
边框：chart border 设为 none
图例：仅必要时显示，放在图表上方（自定义 HTML，不用 Chart.js 默认）
标题字体：加粗，16-18px；标签：12-13px #6B7280
柱间距：categoryPercentage: 0.6, barPercentage: 0.75
```

**图表标题规范：**
- ✅ 洞察型："华东区 Q3 营收同比下降 18%，拖累全国整体表现"
- ❌ 描述型："各区域 Q3 营收对比"

完整代码示例见 `references/chart-examples.md`

---

## Step 4：输出检查清单

- [ ] 已通过 ask_user_input_v0 收集用户偏好？
- [ ] 标题是洞察而非描述？
- [ ] 颜色方案与用户选择匹配？
- [ ] 关键数据点已高亮？
- [ ] 删除了所有装饰性杂乱元素？
- [ ] 有数据来源/时间范围注释？

---

## 参考文件

- `references/color-palettes.md` — 配色方案
- `references/pictograph-icons.md` — 拟物图表 SVG 图标库
- `references/chart-examples.md` — HTML + Chart.js 完整示例
