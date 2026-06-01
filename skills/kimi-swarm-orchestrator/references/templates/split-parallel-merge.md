# 模板：Split-Parallel-Merge（分解-并行-合并）

## 适用场景
任务可横向分解为 3+ 独立子任务，子任务间无数据依赖。典型场景：批量处理、多模块开发、多维度分析。

## 不适用场景
子任务有严格先后顺序、无法预先分解、仅 1-2 个子任务。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator | 1 | 分解任务、分发、合并结果 |
| Worker | 3-N | 执行子任务 |

## 流程图

```
Orchestrator: Decompose into N tasks -> Distribute to Workers
  -> Worker 1 (dim01/, Task A)   --
  -> Worker 2 (dim02/, Task B)     |-- Parallel Execution
  -> Worker 3 (dim03/, Task C)   --
  -> Orchestrator: Merge All Results -> Deliver
```

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Decompose | Orchestrator | 任务描述 + 约束 | 子任务清单 + 输出规范 | 分解合理性 |
| P2-Distribute | Orchestrator | 子任务清单 | Worker 任务包 + dim 目录分配 | Worker 就绪 |
| P3-Execute | Workers(并行) | 任务包 + 上下文 | 各 dim{编号}/ 内的子任务产出 | 无 |
| P4-Collect | Orchestrator | 各 dim 产出 | 完整产出集 | 完整性 |
| P5-Merge | Orchestrator | 产出集 + 合并规则 | output/ 内统一结果 | **Merge Gate** |
| P6-Deliver | Orchestrator | 合并结果 | 最终交付物 | **Quality Gate** |

## 具体示例

**示例 A：多模块代码生成** —— 将电商后台分解为商品/订单/用户三个模块，dim01/dim02/dim03 各自编写后合并为统一代码库。

**示例 B：多维度数据分析报告** —— 将经营数据分析分解为财务/市场/运营三个维度，dim01/dim02/dim03 各自分析后合并为综合报告。

## 变体
| 变体 | 说明 |
|------|------|
| **Nested SPM** | Worker 内部再次使用 SPM |
| **SPM with Review** | 合并后增加 Review 阶段 |
| **Rolling SPM** | 完成一个立即部分合并，增量交付 |
