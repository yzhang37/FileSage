# File Organization Runtime

## 核心判断

系统本质上应该有一个底层运行时：File Organization Runtime。

AI 接口、精确 settings、CLI、agent API 和 GUI 都是运行时上面的控制层。它们不应该各自实现一套判断逻辑。

```text
Natural-language advisor
Advanced settings editor
CLI / JSON / Agent API
Desktop GUI
        |
        v
File Organization Runtime
        |
        v
Analysis / Compare / Report / Safe Plan / Journal
        |
        v
Filesystem / Archive adapters
```

## Runtime 的职责

Runtime 是判定与执行语义的权威。

它负责理解并执行：

- 什么算 `equal`。
- 什么算 `similar`。
- 什么算 `different`。
- 什么情况输出 `unknown`。
- 什么情况输出 `needs_more_analysis`。
- 什么容器应该 `atomic`。
- 什么容器应该 `manifest`。
- 什么容器应该 `shallow`。
- 什么容器应该 `recursive`。
- 什么动作需要 `require_confirmation`。
- 什么结果可以进入 `safe-plan`。

AI 不能绕过 runtime 直接决定移动、删除、覆盖或合并。

## 控制层

### Natural-Language Advisor

把用户的人话翻译成 runtime 能理解的规则草案。

示例：

```text
用户：这些安装镜像不要深入分析，只告诉我是不是同一类东西。
AI：生成规则草案 iso_traversal = atomic_or_manifest，并要求删除动作 require_confirmation。
```

AI 输出必须包括：

- 规则草案。
- 理由。
- 影响范围。
- 风险。
- 可撤销方式。

### Advanced Settings Editor

允许高级用户直接编辑 runtime policy。

示例：

```text
same_hash => equal
same_archive_manifest + close_size => similar
image_phash_distance <= 8 => similar
iso_traversal = atomic
risk_level >= 3 => require_confirmation
```

### CLI / JSON / Agent API

给外部工具和 AI agent 调用。

核心命令：

```text
analyze
compare
report
safe-plan
explain
resume
undo
```

输出必须适合 agent 消费：

- JSON schema 稳定。
- 每个结论有 evidence。
- 每个动作有 risk level。
- 不确定结论用 `unknown` 或 `needs_more_analysis` 表示。
- 计划可以 dry-run。

### Desktop GUI

桌面 GUI 是 shell，不是判定引擎。

GUI 负责：

- 展示报告。
- 展示证据和风险。
- 收集用户确认。
- 编辑 rules/settings。
- 启动、暂停、恢复任务。

GUI 不负责：

- 自己计算 hash。
- 自己遍历容器。
- 自己判断 equal/similar。
- 自己执行删除、移动、覆盖。

## Runtime 输入

Runtime 接收：

- 用户选择的扫描范围。
- 排除项。
- 成本预算。
- runtime policy。
- review decisions。
- workflow 模板。
- 之前的 journal/checkpoint。

## Runtime 输出

Runtime 输出：

- `AnalysisReport`
- `ComparisonResult`
- `SafePlan`
- `RiskAssessment`
- `Evidence`
- `Explanation`
- `JournalEntry`
- `RecoveryState`

## Preference Model

“懂你”必须落到可审计的偏好模型。

Preference Model 记录：

- 用户对 equal/similar 的判断。
- 用户对保留版本的偏好。
- 用户对容器展开深度的偏好。
- 用户对风险等级的容忍度。
- 用户对特定路径、项目、格式的排除或保护规则。

Preference Model 不记录过期的文件系统状态作为真相。硬盘当前状态仍然是唯一真相。

## Review Decision Store

Review Decision Store 记录用户曾经确认过的判断。

示例：

```text
用户确认：JPG 和 PNG 视觉相同可以标为 similar，但不要自动删除。
用户确认：Windows 安装 ISO 只做 manifest-level 比较。
用户确认：同 hash 文件可以归入 exact duplicate group。
用户拒绝：不要把游戏 mod zip 自动合并。
```

这些决定可以影响未来建议，但必须可查看、可编辑、可撤销。

## Policy Compilation

自然语言偏好和高级 settings 最终都要编译成 runtime policy。

```text
Natural language
        |
        v
AI-generated rule draft
        |
        v
User confirmation / editing
        |
        v
Runtime policy
```

高级用户也可以直接编辑 runtime policy。

所有 policy 都必须：

- 可读。
- 可测试。
- 可版本化。
- 可导出。
- 可回滚。
- 能在报告中被引用。

## 不确定性协议

Runtime 不允许用 best effort 掩盖不确定性。

如果证据不足：

```text
status = unknown
reason = insufficient evidence
next = needs_more_analysis | ask_user | skip
```

如果需要更深分析：

```text
status = needs_more_analysis
cost = estimated_time / bytes / recursion_depth
risk = low | medium | high
```

如果风险过高：

```text
status = require_confirmation
risk_level = 3 or 4
reason = destructive or irreversible action
```

## Runtime 与 Journal

Runtime 的动作必须写 journal。

Journal 记录：

- 哪条 policy 触发动作。
- 哪些 evidence 支持动作。
- 哪个用户确认或 review decision 允许动作。
- 执行前文件状态。
- 执行后结果。
- 回滚信息。

Journal 是审计和恢复工具，不是文件系统状态真相。

## 迁移路线

当前 Python 原型阶段：

- Runtime 可以先是 Python module。
- AI advisor 和 settings editor 可以调用同进程 API。
- CLI 输出 JSON。

测试版：

- Python core 保持清晰 runtime 边界。
- PySide6 GUI 通过模块 API 或 sidecar 调用 runtime。

正式版：

- Rust core engine 实现 runtime。
- Flutter desktop UI 通过 FFI、IPC 或 sidecar process 调用 runtime。
- CLI / agent API 继续复用同一个 runtime。

