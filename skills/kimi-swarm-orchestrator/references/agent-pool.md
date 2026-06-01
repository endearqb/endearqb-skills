# Agent Pool Reference — Agent角色池

本文档定义Swarm编排框架中可用的Agent角色。Orchestrator根据任务需要从池中选取角色，而非所有角色都必须出现在每个任务中。

## 角色定义

### Orchestrator (主Agent)

**职责**：唯一全程参与所有Phase的角色。负责任务分析、模式选择、规划监督、Worker部署、结果合并、最终交付。

**决策权限**：全局最高。可覆盖任何Worker的决策，可调整计划，可终止任务。

**能力要求**：必须能够：创建子Agent、读写文件、运行Shell命令、管理目录结构。

**出现频率**：100%的任务。

### Planner (规划师)

**职责**：编写规划文档。将用户需求转化为可执行的技术/内容规划。

**触发条件**：任务复杂度高、需要领域专业知识做规划、Orchestrator不直接具备规划能力时。

**工作方式**：作为Orchestrator的子Agent在Phase 2启动，读取用户请求和上下文，产出规划文档。

**典型任务**：
- 研究报告：维度分解、搜索策略设计
- 代码项目：架构设计、模块划分、接口定义
- 网站项目：页面结构、视觉方向、技术选型
- PPT项目：大纲设计、视觉方案

**出现频率**：约60%的任务（复杂任务需要）。

### Scaffold (脚手架搭建者)

**职责**：搭建项目基础设施，创建共享组件和公共配置，为Worker提供可继承的工作基础。

**触发条件**：项目型任务（代码开发、网站建设）需要统一的基础设施时。

**工作方式**：作为Orchestrator的子Agent在Phase 3启动，先于Worker完成基础设施搭建。

**典型产出**：
- 项目初始化和依赖安装
- 共享UI组件（导航栏、页脚、布局）
- 配置文件和主题定义
- 路由框架和存根页面
- 公共资源（图片、字体、媒体文件）

**出现频率**：约50%的任务（项目型任务需要）。

### Worker (执行者)

**职责**：执行具体任务，产出可交付物。

**工作方式**：在Phase 4并行启动，每个Worker负责规划文档中分配的一个或多个子任务。

**Worker分组策略**：

| 分组方式 | 适用场景 | 示例 |
|----------|----------|------|
| 按模块分组 | 代码项目 | Worker A负责用户模块，Worker B负责订单模块 |
| 按页面分组 | 网站项目 | Worker A负责首页+关于，Worker B负责服务+定价 |
| 按维度分组 | 研究项目 | Worker A负责市场维度，Worker B负责技术维度 |
| 按阶段分组 | 内容项目 | Worker A负责第1-3章，Worker B负责第4-6章 |

**Worker命名约定**：`{任务}-{角色}-{编号}`，如 `research-worker-01`、`webapp-worker-home`。

**出现频率**：100%的多Agent任务（至少1个）。

### Verifier (验证者)

**职责**：质量检查、测试、验证产出物符合规划文档的要求。

**触发条件**：质量要求高的任务，或Phase 6合并后需要独立验证时。

**工作方式**：作为Orchestrator的子Agent在Phase 7启动，读取规划文档和最终产出，执行验证检查。

**验证类型**：
- **完整性验证**：所有要求的组件是否都存在
- **一致性验证**：各Worker产出之间的接口是否正确连接
- **质量验证**：产出是否符合规划文档的质量标准
- **格式验证**：文件格式、命名、结构是否符合规范

**出现频率**：约40%的任务（高质量要求任务需要）。

## 角色交互图

```
Orchestrator
  ├── Planner (Phase 2, 可选)
  ├── Scaffold (Phase 3, 可选)
  ├── Worker-01 (Phase 4)
  ├── Worker-02 (Phase 4)
  ├── Worker-03 (Phase 4)
  ├── ...
  └── Verifier (Phase 7, 可选)

交互规则：
- Orchestrator → 任何角色：指令下达
- Planner → Orchestrator：规划文档交付
- Scaffold → shared/ 目录：共享资源创建
- Worker → dim{编号}/ 目录：产出写入
- Verifier → Orchestrator：验证报告
- Worker X ↔ Worker Y：禁止直接通信
```

## Agent能力矩阵

| 能力 | Orchestrator | Planner | Scaffold | Worker | Verifier |
|------|:----------:|:-------:|:--------:|:------:|:--------:|
| 创建子Agent | ✅ | ❌ | ❌ | ❌ | ❌ |
| 读写文件 | ✅ | ✅ | ✅ | ✅(仅限dim内) | ✅(只读) |
| Shell命令 | ✅ | ❌ | ✅ | ✅ | ❌ |
| 搜索/浏览 | ✅ | ✅ | ❌ | 按需 | ❌ |
| 决策任务范围 | ✅ | 设计范围 | 实现范围 | 范围内 | 质量判定 |

## 最小Agent配置

| 模式 | 最小Agent集合 |
|------|-------------|
| Mode A (Full) | Orchestrator + Planner + Scaffold + 3+ Workers |
| Mode B (Compact) | Orchestrator + 2-3 Workers |
| Mode C (Sequential) | Orchestrator + 1 Worker |
| Mode D (Selective) | Orchestrator + 1-N Workers |
