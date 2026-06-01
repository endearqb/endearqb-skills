# 模板：Explore-Dive-Verify（探索-深入-验证）

## 适用场景
范围不明确，需先建立全局认知再深入，且多维度间需交叉验证。典型场景：深度研究、技术调研、竞争分析。

## 不适用场景
范围明确无需探索、仅单一维度、时间极短。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator | 1 | 路由选择、分解、交叉验证 |
| Explorer | 1（可复用 Orchestrator） | 快速扫描全景 |
| Worker | 2-N | 各维度深度分析 |

## 流程图

```
Orchestrator: Quick Scan (Landscape)
  -> Decompose into Dimensions
  -> Worker 1 (dim01/, Deep Dive A)    --
  -> Worker 2 (dim02/, Deep Dive B)      |-- Parallel Deep Dive
  -> Worker N (dimN/,  Deep Dive N)    --
  -> Orchestrator: Cross-Verify
       -> Conflict? -> Yes: Resolve -> Extract Insights
                     -> No:  Extract Insights
  -> Deliver
```

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Scan | Explorer | 研究主题 + 初始问题 | 全景概览 + 关键领域清单 | 上下文充分 |
| P2-Decompose | Orchestrator | 全景概览 | 分析维度 + Worker 任务 + dim 分配 | 维度 MECE |
| P3-Dive | Workers(并行) | 维度任务 + 上下文 | 各 dim{编号}/ 内深度报告 | 深度达标 |
| P4-Verify | Orchestrator | N 份维度报告 | 一致性评估 + 冲突清单 | 冲突检测 |
| P5-Resolve | Orchestrator+Worker | 冲突清单 | 已解决冲突记录 | 冲突全解 |
| P6-Extract | Orchestrator | 验证后报告集 | 综合洞察报告（output/） | **Quality Gate** |

## 具体示例

**示例 A：技术选型深度研究** —— 扫描数据库领域后分解为性能/生态/运维/成本四维度，4 Worker 并行深入，交叉验证后综合权衡输出选型建议。

**示例 B：市场竞争格局分析** —— 扫描赛道参与者后分解为产品能力/市场份额/融资/技术壁垒四维度，交叉验证后解决数据矛盾输出格局报告。

## 变体
| 变体 | 说明 |
|------|------|
| **Recursive EDV** | 某维度再次使用 EDV |
| **EDV with Expert** | 引入领域专家验证 |
| **Streaming EDV** | 探索与深入交替进行 |
