---
name: swarm-orchestrator
description: >
  通用多智能体编排框架。用于任何需要多Agent协作的任务：研究报告、代码开发、内容创作、数据分析、设计评审等。提供稳定的Agent协调、并行执行、错误恢复和结果合并能力。当任务需要多个Agent协作时，加载此技能作为底层编排框架。
  
  触发条件：任务满足以下任一特征时激活此技能：
  - 任务可分解为3+个可独立执行的子任务
  - 任务需要顺序规划和并行执行混合模式
  - 任务产出物需要多个独立部分最后整合为整体
  - 任务复杂度高，单Agent执行时间超过合理阈值
  - 任务涉及多个领域知识，需要不同角色的Agent协作
  
  不适用于：单步查询、简单问答、仅需单Agent即可完成的简单任务。
---
# Swarm Orchestrator — 通用多智能体编排框架

## Overview

Swarm Orchestrator 是一个通用多Agent编排框架，从6个生产级Swarm技能中提取通用模式，适用于任何需要多Agent协作的任务类型。

**核心思想**：将复杂任务分解为**文档先行规划**、**并行工作执行**、**顺序结果合并**的三段式流程，通过 `dim{编号}/` 目录实现零冲突隔离，通过模式选择适配不同复杂度。

**与其他技能的关系**：此技能提供编排的**底层框架**。专用技能（如 deep-research-swarm、vibecoding-webapp-swarm）可以基于此框架构建，添加领域特定的规则和工具。

## 路径约定

本技能**不硬编码**任何绝对输出路径。所有输出位置遵循以下优先级：

1. **工作目录 `agents.md`**（最高优先级）：如果项目根目录存在 `agents.md`（或 `CLAUDE.md`），读取其中的路径约定
2. **任务根目录**：以当前工作目录为基准，在其下创建 `{任务名}/` 子目录作为任务根
3. **Worker 隔离目录**：任务根目录下以 `dim01/`、`dim02/`、... 区分各 Worker 的独立工作空间

下文中凡出现 `{任务根}/` 均指上述相对路径，**不要**替换为绝对路径。

## Core Principles (编排原则)

1. **Orchestrator owns coordination** — 主Agent负责任务分析、模式选择、Worker部署、结果合并和最终交付。Worker只执行被分配的任务。
2. **Workers own execution** — Worker Agent负责其被分配范围内的完整执行，包括质量控制和错误恢复。Worker不自主决定做什么，但自主决定怎么做。
3. **Document-first gating** — 在任何执行开始前，Orchestrator必须先产出规划文档（设计文档/规格/任务分解）。文档是Gate — 未完成前不进入执行阶段。
4. **Directory-based isolation** — 每个Worker拥有独立的 `dim{编号}/` 目录，互不干扰。Worker之间不直接通信，只通过文件系统间接协调。
5. **Fidelity to specification** — Worker必须忠实执行Orchestrator的规划文档，不得擅自修改接口、调整范围或改变设计。
6. **Graceful degradation** — 单个Worker失败不影响整体流程。Orchestrator负责重试、重新分配或降级处理。
7. **Observable execution** — 每个Worker必须将结果写入其 `dim{编号}/` 目录，Orchestrator通过读取文件监控进度，不依赖Worker的状态报告。
8. **Bounded iteration over one-shot perfection** — 当任务质量需要打磨时，允许 Orchestrator 在交付前运行**有界精炼回路**（见 Refinement Loop 章节），但循环必须满足三个硬约束：**迭代上限**、**收敛判据**、**无改进即停**。循环只发生在 Orchestrator 层（重新部署 Worker 修复具体缺口），单个 Worker 自身永不循环。**没有终止条件的循环视为缺陷，不得交付。**

## Architecture

### Agent Role Model

Orchestrator 根据任务需要，从Agent池中分配角色。详见 `references/agent-pool.md`。


| 角色                        | 职责                          | 典型数量  | 决策权限  |
| ------------------------- | --------------------------- | ----- | ----- |
| **Orchestrator** (主Agent) | 任务分析、模式选择、规划、Worker部署、合并、交付 | 1     | 全局决策  |
| **Planner/Designer**      | 规划文档、设计文档、规格书编写             | 0-1   | 设计决策  |
| **Scaffold/Setup**        | 基础设施搭建、共享组件、项目初始化           | 0-1   | 实现决策  |
| **Worker** (执行者)          | 并行执行具体任务                    | 1-10+ | 范围内决策 |
| **Verifier**              | 验证、测试、质量检查                  | 0-1   | 质量判定  |


### Workflow Pattern

所有Swarm工作流遵循统一模板。模板选择指南见 `references/template-index.md`，各模板详情见 `references/templates/` 目录下对应文件。Orchestrator 先读 template-index.md 选择模板，再按需加载具体模板文件。

```
Phase 1: 任务分析 & 模式选择 (Orchestrator)
  │
  ▼
Phase 2: 规划 & 文档创建 (Orchestrator ± Planner)
  │
  ▼
Phase 3: 环境搭建 (Orchestrator ± Scaffold)
  │
  ▼
Phase 4: Worker并行部署 (Orchestrator 启动 Workers)
  │
  ▼
Phase 5: 监控 & 自适应控制 (Orchestrator)
  │
  ▼
Phase 6: 结果聚合 & 合并 (Orchestrator)  ◄─────────────┐
  │                                                    │
  ▼                                                    │
Phase 7: 验证 & 交付 (Orchestrator ± Verifier)         │
  │                                                    │
  ├─ [可选] 精炼回路: 质量未达标 且 未到迭代上限         │
  │         且 上一轮有改进 → 选择性重部署 Worker 修复 ──┘
  │
  ▼ 质量达标 / 触达迭代上限 / 无改进
STOP
```

默认情况下 Phase 7 直接 STOP（稳定瀑布）。**精炼回路是可选层**，仅在选定模式开启时介入，见 Mode Selection 与 Refinement Loop 章节。

### Error Recovery

错误恢复策略和重试规则。详见 `references/error-recovery.md`。

## Workflow Lifecycle

### Phase 1: Task Analysis &amp; Mode Selection

**Goal**: 分析任务特征，选择执行模式。

**Input**: 用户请求、上传文件、上下文信息。

**Process**:

1. 读取工作目录 `agents.md`（如果存在），获取路径约定和项目上下文
2. 评估任务复杂度：子任务数量、依赖关系、领域跨度
3. 检查是否有用户上传文件（影响路由选择）
4. 选择执行模式（见 Mode Selection 章节）
5. 初始化输出目录：`mkdir -p {任务根}/`

**Output**: 选择的模式声明 + 理由说明。

**Rules**:

- **[CRITICAL]** 模式选择一旦确定，不得在执行过程中更改。
- 当不确定时，选择更保守的模式（更多Worker → 更精简）。

---

### Phase 2: Planning &amp; Document Creation

**Goal**: 产出规划文档，作为后续所有阶段的单一事实来源。

**Input**: 用户请求、Phase 1的模式选择、任何上传文件。

**Process**:

1. **信息收集**（如需要）：搜索、浏览URL、分析文件，将结果写入 `{任务根}/info.md`
2. **文档创建**：由Orchestrator或Planner子Agent编写规划文档。文档内容因任务类型而异：


| 任务类型 | 规划文档  | 关键内容             |
| ---- | ----- | ---------------- |
| 研究报告 | 研究计划  | 维度分解、搜索策略、来源要求   |
| 代码开发 | 规格书   | 架构、模块边界、接口定义、数据流 |
| 内容创作 | 大纲+设计 | 结构、风格、每页/章内容要点   |
| 数据分析 | 分析计划  | 数据集、分析方法、可视化要求   |


3. **文档审查**：Orchestrator审查规划文档的完整性和可执行性

**Output**: 规划文档保存至 `{任务根}/plan.md`。

**Rules**:

- **[CRITICAL]** 规划文档未完成前，绝不进入Phase 3。
- **[CRITICAL]** 规划文档是Worker的唯一输入源。Orchestrator不得在Worker执行后补充新指令。
- 规划文档必须包含Worker分配方案 — 哪些任务由哪个Worker执行，以及对应的 `dim{编号}/` 目录。

---

### Phase 3: Environment Setup

**Goal**: 搭建执行环境，确保Worker可以零冲突并行工作。

**Input**: Phase 2的规划文档。

**Process**:

1. **创建隔离目录**：为每个Worker创建独立的 `dim{编号}/` 目录
  ```bash
   mkdir -p {任务根}/dim01 {任务根}/dim02 {任务根}/dim03
  ```
2. **搭建共享资源**（如需要，由Scaffold Agent执行）：
  - 将共享组件、公共配置、模板放入 `{任务根}/shared/` 目录
  - 安装依赖、配置工具链
  - 生成共享资源（图片、字体等）
3. **分发共享资源**：将 `shared/` 中Worker需要的文件复制到各 `dim{编号}/` 目录，或在Worker指令中指明读取 `shared/` 的路径

**Output**: 可工作的隔离目录 + 共享资源。

**Rules**:

- **[CRITICAL]** 每个Worker必须在自己的 `dim{编号}/` 目录内工作，不得写入其他Worker的目录。
- **[CRITICAL]** Scaffold阶段完成后才能启动Worker — Worker需要继承Scaffold产出的共享资源。
- `shared/` 目录在Worker执行阶段为**只读** — Worker不得修改共享资源。

---

### Phase 4: Worker Deployment

**Goal**: 并行启动所有Worker，执行具体任务。

**Input**: 规划文档、环境设置完成的目录结构。

**Process**:

1. **编写Worker指令**：为每个Worker编写任务提示，必须包含：
  - **(1) Mission**：任务范围、输出要求、质量指标
  - **(2) Context**：规划文档的相关部分、前置阶段的关键发现
  - **(3) Workspace**：工作目录路径（`{任务根}/dim{编号}/`）
  - **(4) Boundaries**：不得修改的文件/范围（`shared/` 目录、其他Worker的 `dim{编号}/` 目录）
  - **(5) Output**：输出文件路径、格式要求
2. **并行启动**：在同一条消息中启动所有Worker（多个 `task` 调用）
3. **Worker执行**：
  ```bash
   # Worker在自己的dim目录内工作
   cd {任务根}/dim{编号}
   # 执行任务...
   # 完成后在目录内留下产出文件
  ```

**Output**: 每个Worker在其 `dim{编号}/` 目录中产出结果文件。

**Rules**:

- **[CRITICAL]** Worker启动顺序：先启动Scaffold（如需要），Scaffold完成后再并行启动Workers。
- **[CRITICAL]** 每个Worker的提示必须独立完整 — Worker之间不共享上下文。
- **[CRITICAL]** Worker完成后必须确保所有产出文件在其 `dim{编号}/` 目录内，然后立即返回。不得运行验证、服务器或浏览器。

---

### Phase 5: Monitoring &amp; Adaptive Control

**Goal**: 监控Worker进度，处理失败和超时。

**Input**: 各 `dim{编号}/` 目录的文件产出状态。

**Process**:

1. **状态检查**：检查每个Worker的 `dim{编号}/` 目录是否有预期的输出文件
  ```bash
   ls -la {任务根}/dim01/
   ls -la {任务根}/dim02/
  ```
2. **超时处理**：Worker在合理时间内未完成 → 记录为超时，启动备用Worker
3. **失败恢复**：Worker失败 → 根据错误类型选择策略：
  - **可重试错误**（网络、临时资源不可用）：重启同一Worker
  - **逻辑错误**（规划缺陷）：记录问题，继续其他Worker，Phase 6时处理
  - **环境错误**（依赖缺失）：修复环境后重启
4. **自适应调整**：如多个Worker遇到同类问题，Orchestrator应更新剩余Worker的指令

**Output**: 每个Worker的状态报告（成功/失败/超时 + 产出摘要）。

**Rules**:

- **[CRITICAL]** 单个Worker失败不得阻塞整体流程。Orchestrator必须继续处理其他Worker的结果。
- **[CRITICAL]** 不得在没有明确理由的情况下无限重试。最多重试2次。

---

### Phase 6: Result Aggregation &amp; Merge

**Goal**: 合并所有Worker的产出，解决冲突，形成统一结果。

**Input**: 所有 `dim{编号}/` 目录的产出、Phase 5的状态报告。

**Process**:

1. **读取产出**：Orchestrator读取每个 `dim{编号}/` 目录中的输出文件
2. **合并策略选择**：


| 场景            | 合并策略 | 操作                                    |
| ------------- | ---- | ------------------------------------- |
| 各Worker产出独立文件 | 直接汇总 | 将各 `dim{编号}/` 中的文件复制到 `{任务根}/output/` |
| 需要拼接为单文件      | 按序拼接 | 按规划文档顺序拼接各Worker产出                    |
| 产出需要交叉整合      | 手动整合 | Orchestrator读取所有产出后，重新组织结构            |


3. **冲突解决**：如果多个Worker产出了重叠内容，Orchestrator手动解决，优先保留各Worker的完整产出
4. **集成**：连接各Worker产出的接口点 — 如路由注册、索引创建、汇总生成

**Output**: 合并后的统一产出，位于 `{任务根}/output/` 目录。

**Rules**:

- **[CRITICAL]** 合并时，不得丢弃任何Worker的产出。有争议的部分应保留备选，由Orchestrator决定最终版本。
- **[CRITICAL]** 合并后必须进行集成检查 — 确保各Worker产出之间的接口正确连接。

---

### Phase 7: Verification &amp; Delivery

**Goal**: 验证最终产出质量，交付给用户。

**Input**: 合并后的统一产出。

**Process**:

1. **完整性检查**：确认所有规划文档中要求的产出都已包含
2. **质量检查**：运行测试、验证格式、检查约束条件，产出质量评分/问题清单
3. **精炼判定**（仅当模式开启精炼回路时）：依据 Refinement Loop 章节的三条硬约束判断是否回到 Phase 6 再做一轮；否则跳过
4. **最终构建**（如需要）：构建生产版本、生成交付物
5. **交付**：将最终结果输出到 `agents.md` 指定的交付目录（或 `{任务根}/output/`）
6. **STOP**：交付后停止。不打开URL、不截图、不做计划外验证。

**Output**: 最终交付物 + 完成状态报告。

**Rules**:

- **[CRITICAL]** 禁止**无界**的部署后循环 — 不得反复"再检查一遍"式地空转。唯一允许的循环是 Refinement Loop 章节定义的**有界精炼回路**（有迭代上限、收敛判据、无改进即停）。回路结束后立即 STOP。
- **[CRITICAL]** 精炼回路默认**关闭**；仅在 Phase 1 选定的模式显式开启时才可进入。
- **[CRITICAL]** 最终交付物必须通过完整性检查 — 缺少任何必要组件不得交付。

## Refinement Loop (精炼回路)

精炼回路是一个**可选、有界**的"批评→修复→再合并"循环，作用在**已成功合并的产出**上，用于打磨质量（区别于 Error Recovery —— 后者修复的是失败的 Worker，前者改进的是成功但不够好的产出）。它把 Design-Delegate-Iterate 模板里局部的迭代能力，提升为框架级、带安全护栏的能力。

### 何时开启


| 情况                          | 是否开启   |
| --------------------------- | ------ |
| 产出有明确质量标准、需要打磨（报告、UI、标准化文档） | 建议开启   |
| 一次性产出即可、时间紧、各部件无关联          | 关闭（默认） |
| 用户明确要求"一次交付""不要反复改"         | 强制关闭   |


开启方式：在 Phase 1 声明模式时一并声明 `refine: on, max_iterations: N`（见 Mode Selection）。

### 三条硬约束（缺一不可）

1. **迭代上限**：默认 `max_iterations = 2`，绝对不超过 3。达到上限即交付当前最佳版本。
2. **收敛判据**：每轮必须有可度量的质量信号（质量评分、问题清单条数、测试通过率等）。判据写入 `{任务根}/refine_log.md`。
3. **无改进即停**：若某轮相对上一轮**质量信号无提升**（或提升低于设定阈值），立即停止，不再迭代——防止抖动空转。

### 回路流程

```
Phase 7 质量检查产出 问题清单 + 质量评分
  │
  ▼
进入精炼判定:
  ├─ 质量达标?                → 是 → STOP 交付
  ├─ 已达 max_iterations?      → 是 → 交付当前最佳版本 + 标注遗留问题
  ├─ 本轮相比上轮无改进?        → 是 → 回滚到上轮最佳版本 → STOP
  └─ 以上皆否 → 回到 Phase 6:
        用 Mode D (Selective) 只对"有问题的 dim{编号}/"重部署 Worker 修复
        → 重新合并 → 回到 Phase 7 再评估 (iteration += 1)
```

**Rules**:

- **[CRITICAL]** 每轮只修复问题清单里**具体、已定位**的缺口（选择性重部署），不得整体重做、不得借机扩大范围。
- **[CRITICAL]** 每轮把 `iteration`、质量信号、本轮改动写入 `{任务根}/refine_log.md`，供"无改进即停"判断。
- **[CRITICAL]** 精炼回路**不是模式变更** —— 不违反"模式一旦确定不得更改"；它在选定模式内部运行。
- **[CRITICAL]** 回路只在 Orchestrator 层循环。被重部署的 Worker 仍是单次执行、完成即返回，绝不自带循环。

### 与 ReAct 式自适应的关系

Adaptive-Routing 模板提供的是**执行期**的"评估→重路由"自我发现（reason→act→observe→re-decide）；Refinement Loop 提供的是**交付期**的质量迭代。两者都受同一套护栏约束——必须有上限和终止判据。可组合：执行期用 Adaptive-Routing 找对路径，交付期用 Refinement Loop 打磨质量。

## Mode Selection

Orchestrator在Phase 1根据任务特征选择执行模式：


| 条件                   | 模式                         | Worker数 | 精炼回路默认     | 适用场景            |
| -------------------- | -------------------------- | ------- | ---------- | --------------- |
| 任务复杂度高、多个独立子任务、领域跨度大 | **Mode A (Full Swarm)**    | 3-10+   | 可开启        | 研究报告、大型项目、复杂系统  |
| 中等复杂度、子任务间有轻度依赖      | **Mode B (Compact Swarm)** | 2-3     | 可开启        | 中型项目、多页面网站、模块开发 |
| 简单任务或需要严格顺序执行        | **Mode C (Sequential)**    | 1       | 关闭         | 单功能开发、简单分析      |
| 增量更新、部分重试、修复         | **Mode D (Selective)**     | 1-N     | —（本身即修复机制） | 补丁、Bug修复、部分重做   |


**精炼回路声明**：Phase 1 声明模式时，可附加 `refine: on/off` 与 `max_iterations: N`（默认 off；开启时 N 默认 2、上限 3）。例如：`Mode A, refine: on, max_iterations: 2`。Mode D 本身就是精炼回路调用的"选择性重部署"机制，无需单独开启。

**模式升级/降级规则**：

- Mode B在执行中发现任务比预期复杂 → 将剩余工作拆分为更多Worker
- Mode A中部分Worker因依赖关系无法并行 → 将其转为顺序执行
- **[CRITICAL]** 模式变更必须在Phase 2完成前决定，Phase 3后不得更改模式。

## Agent Communication Protocol

Worker之间不直接通信。所有协调通过以下机制间接完成：


| 机制               | 用途                        | 写入者          | 读取者          |
| ---------------- | ------------------------- | ------------ | ------------ |
| 规划文档 (`plan.md`) | 任务定义和范围                   | Orchestrator | 所有Worker     |
| `dim{编号}/` 目录产出  | 进度信号和产出交付                 | Worker       | Orchestrator |
| `shared/` 目录     | 共享资源（图片、配置、模板）            | Scaffold     | 所有Worker（只读） |
| `refine_log.md`  | 迭代轮次、质量信号、改动记录（"无改进即停"依据） | Orchestrator | Orchestrator |
| 文件命名约定           | 文件归属标识                    | Worker       | Orchestrator |


## File &amp; Output Conventions

### 目录结构

```
{任务根}/                        # 任务根目录（相对于工作目录）
├── plan.md                     # 规划文档（Phase 2产出）
├── info.md                     # 研究/分析结果（可选）
├── refine_log.md               # 精炼回路日志（仅 refine:on 时产出）
├── shared/                     # 共享资源目录（Scaffold产出）
│   ├── components/             # 共享组件
│   ├── config/                 # 公共配置
│   └── assets/                 # 共享资源文件
├── dim01/                      # Worker 01 工作目录
│   └── ...                     # Worker 01 的产出
├── dim02/                      # Worker 02 工作目录
│   └── ...                     # Worker 02 的产出
├── dim03/                      # Worker 03 工作目录
│   └── ...                     # Worker 03 的产出
└── output/                     # 最终合并产出目录
```

### 文件命名规范


| 文件类型     | 命名模式                   | 示例                         |
| -------- | ---------------------- | -------------------------- |
| Worker产出 | `dim{编号}/` 内按任务自然命名    | `dim01/market_analysis.md` |
| 验证结果     | `{任务}_verification.md` | `project_verification.md`  |
| 合并报告     | `{任务}_merge_report.md` | `project_merge_report.md`  |


## Quick Start Templates

### 启动新Swarm任务的最小流程

```
1. Phase 1: 读取 claude.md → 确定模式 + 是否 refine:on → 声明模式
2. Phase 2: 编写 plan.md → 保存到 {任务根}/
3. Phase 3: 创建 dim{编号}/ 目录 → 准备 shared/（如需要）
4. Phase 4: 并行启动 Workers（各自在 dim{编号}/ 内工作）
5. Phase 5: 监控 → 处理失败
6. Phase 6: 读取各 dim{编号}/ 产出 → 合并到 output/
7. Phase 7: 验证 → [若 refine:on] 未达标且未到上限且有改进 → 回 Phase 6 选择性修复 → 交付 → STOP
```

### Worker任务提示模板

```
工作目录:
  {任务根}/dim{编号}/

任务范围:
  {具体任务描述}

输入:
  - 规划文档: {任务根}/plan.md
  - 共享资源: {任务根}/shared/（只读）
  - 相关上下文: {文件路径}

边界:
  - 不得修改: shared/ 目录、其他 dim{编号}/ 目录
  - 只在 dim{编号}/ 内创建/修改文件

输出:
  - 文件路径: {任务根}/dim{编号}/{输出文件名}
  - 格式要求: {格式说明}

完成后:
  确认所有产出文件在 dim{编号}/ 目录内。
  返回执行摘要。
```

## Integration with Other Skills

此技能作为底层编排框架，可与专用技能组合使用：


| 组合方式       | 说明                       | 示例                                               |
| ---------- | ------------------------ | ------------------------------------------------ |
| **作为基础框架** | 专用技能继承此框架的Phase定义，添加领域规则 | deep-research-swarm 继承7-Phase流程，添加研究维度分解和交叉验证    |
| **作为协调层**  | 专用技能提供领域工具，此技能提供协调逻辑     | vibecoding-webapp-swarm 提供React工具链，此技能管理Worker部署 |
| **独立引用**   | 复杂任务加载此技能获取编排指导          | 数据分析任务引用此技能分解为并行分析维度                             |


**加载顺序**：先加载此技能获取编排框架，再加载专用技能获取领域工具。Orchestrator读取两个技能后，按此技能的Phase流程执行，在适当步骤调用专用技能的领域规则。