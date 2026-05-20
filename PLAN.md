# PLAN.md

这份计划记录项目真正要解决的问题：File Organizer 不只是按扩展名搬文件，而是一个可中断、可恢复、可解释的文件分析与整理系统。

## 核心定位

File Organizer 的目标是帮助用户理解、比较、去重、归档和整理复杂文件集合。

整理动作不是唯一目标。用户完全可以只运行一次 DryRun / analysis-only，让系统输出专业分析报告，然后自己决定怎么处理。

它需要处理普通文件夹，也需要处理嵌套容器，例如 ZIP、CAB、7z、RAR、tar、ISO，以及未来可能出现的磁盘镜像、备份包和应用专用包格式。

这个系统必须允许用户定义：

- 什么叫两个文件“相等”。
- 什么叫两个文件“相似”。
- 什么情况下一个容器应该被展开分析。
- 什么情况下一个容器应该被当成原子文件。
- 对相等文件、相似文件和不确定文件分别执行什么工作流。
- 是否只产出报告，而不执行任何整理动作。

## 基本原则

### 1. 硬盘是真相

文件系统每天都在变化，所以不能把数据库设计成权威缓存。

本项目可以使用轻量数据库，但它只应该记录：

- 已经完成过哪些任务。
- 某次分析的输入指纹。
- 某次分析的输出摘要。
- journal 和回滚所需信息。
- 中断恢复所需的队列、检查点和错误信息。

数据库不应该让系统误以为“昨天看到的文件状态就是今天的文件状态”。任何危险动作执行前都必须重新验证文件是否仍然满足当时的前提条件。

### 2. 可随时中断，随时恢复

任务可能非常重，不能假设一次跑完。

设计上要支持：

- 每个任务小粒度、幂等、可重试。
- 每个阶段都有 checkpoint。
- 中断后重启时重新读取当前文件系统。
- 对已经变化的文件重新排队，而不是盲目信任旧结果。
- 对无法继续的任务保留可读错误，不阻塞整个项目。

### 3. DryRun 和专业报告是一等产品模式

DryRun 不应该只是“执行前预览”。它本身就是一个完整工作流。

很多用户只想知道：

- 哪些文件完全相等。
- 哪些文件高度相似。
- 哪些文件只是可能相关，但证据不足。
- 哪些文件系统认为必须保留。
- 哪些文件可能是低质量副本。
- 哪些容器文件几乎是同一种东西。
- 哪些 ISO 很像 Windows XP 安装镜像。
- 哪些压缩包或镜像很像某个游戏、软件或资料集的不同版本。

报告应该给出专业分析，而不是直接逼用户整理：

- 分组结果。
- 证据来源。
- 置信度。
- 风险等级。
- 建议保留项。
- 可选处理方案。
- 仍需人工确认的问题。
- 进一步深度分析的成本和收益。

用户看完报告后，可以选择：

- 什么都不做，自己手动处理。
- 保存报告。
- 调整规则后重新分析。
- 把某些报告项转成整理计划。
- 只对低风险项执行自动工作流。

### 4. 分析是渐进式的

不要一上来就深度遍历所有内容。

分析应该从便宜到昂贵逐层升级：

1. 路径、文件名、扩展名、大小、mtime、inode 等元数据。
2. 快速哈希或分块采样。
3. 完整内容哈希。
4. 容器文件清单。
5. 容器内部递归树。
6. 媒体特征、图片感知哈希、音视频指纹。
7. AI 辅助判断和策略建议。

只有当某个工作流真的需要更高成本信息时，才进入更深层分析。

### 5. 相等和相似是用户策略

“相等”和“相似”不是固定概念。

例如：

- 两个文件 byte hash 完全相同，可以被某个策略定义为相等。
- 两张图片内容看起来完全一样，但一个是 JPG，一个是 BMP，可以被某个策略定义为相似。
- 两个 ZIP 文件可以按完整展开后的子文件 hash 树判断相等。
- 两个 ZIP 文件也可以只按内部清单、大小和时间戳判断相似。
- 两个 Windows XP 安装 ISO 可能只比较卷标、目录清单和关键文件，而不展开每个文件做完整 hash。

系统应该提供模板，但不把用户锁死。

### 6. 容器可以是节点，也可以是原子

一个 ZIP 或 ISO 既可以被看作文件，也可以被看作虚拟文件夹。

系统需要为每个容器决定 traversal policy：

- `atomic`: 当作单个文件。
- `manifest`: 只读取内部清单。
- `shallow`: 读取一层内容摘要。
- `recursive`: 递归展开分析。
- `custom`: 用户或模板定义的专门策略。

这个策略可以来自用户规则，也可以来自系统建议，但危险或昂贵策略必须可解释、可确认。

### 7. AI 是顾问，不是裁判

AI 可以帮助识别模式，例如：

- 这两个文件很像 Windows 安装镜像。
- 这些 ZIP 很像同一个项目的不同导出版本。
- 这个目录可能是软件安装包，不建议深度遍历。
- 这批图片可能是同一张图的不同格式或不同质量版本。
- 这些镜像或压缩包很像同一个游戏、软件或系统安装介质的不同版本。

但 AI 不能直接承担删除、覆盖、合并的责任。

AI 的输出应该是建议：

- 建议策略。
- 置信度。
- 理由。
- 可选方案。
- 预计成本。
- 风险提示。

最终选择权属于用户和用户定义的 workflow。

### 8. 交付形态必须是桌面应用

最终用户应该拿到真正的桌面程序，而不是被要求在浏览器里授权一堆文件权限。

目标交付：

- macOS: `.app`，正式发布需要代码签名和 notarization。
- Windows: `.exe` 和 installer，正式发布需要代码签名和升级策略。

浏览器或 WebView 不作为默认产品路线。即使未来 UI 技术包含 WebView，文件扫描、hash、容器分析、journal、执行和恢复也必须放在本地 core engine 中。

发布工程需要明确规划：

- 应用打包。
- installer。
- 代码签名。
- macOS notarization。
- 自动更新或手动升级路径。
- 崩溃日志和诊断日志位置。
- 用户配置和 journal 存储位置。
- 卸载时是否保留用户配置和 journal。

权限模型也必须明确规划：

- 只读扫描权限。
- 报告导出权限。
- Documents、Desktop、Downloads 访问。
- 外接硬盘和网络盘访问。
- 移动、复制、删除、覆盖等危险动作权限。
- 用户撤销授权或路径失效后的恢复行为。

### 9. 开发与语言路线

当前仓库先保留 Python 原型，用来快速验证：

- 可中断任务模型。
- 指纹和比较策略。
- 专业分析报告。
- journal 和恢复语义。
- CLI 和早期 GUI 交互。

测试版路线：

- Python CLI。
- Python core。
- PySide6 / Qt for Python 桌面 UI。
- 打包 macOS `.app` 和 Windows `.exe`。

正式版方向：

- Rust core engine：负责扫描、hash、容器 adapter、比较策略、journal、恢复和报告模型。
- Flutter desktop UI：负责跨平台界面、报告展示、确认流程和规则配置。

核心原则：UI 可以替换，core engine 不能绑死在 UI 框架里。

UI shell 和 core engine 的通信方式可以在不同阶段演进：

- 原型期：同进程 Python API。
- 测试版：独立 core module 或 sidecar process。
- 正式版：Rust core 通过 FFI、IPC 或 sidecar process 暴露能力。

无论采用哪种通信方式，UI 层都不能直接实现扫描、hash、容器遍历、journal、删除或移动。

### 10. Windows 和 macOS 都是一等平台

Windows 开发环境计划使用 MSYS2 + zsh，不以 PowerShell 作为主要开发环境。

但应用本身必须支持原生 Windows 行为：

- Windows drive path，例如 `C:\Users\...\Downloads`。
- MSYS2 path，例如 `/c/Users/...`，至少在开发工具链中友好处理。
- 大小写不敏感文件系统。
- Windows 保留文件名。
- 长路径。
- 非 ASCII 路径。
- 文件名包含空格。

所有实现都应使用语言标准路径 API，不要手写路径分隔符。

## 系统模块

### Scanner

读取当前文件系统，发现候选节点。

职责：

- 枚举目录。
- 识别普通文件、目录、容器文件。
- 生成当前观察结果。
- 跳过用户排除项。
- 产生可恢复任务，而不是一次性做完全部分析。

### Virtual Filesystem Adapter

把不同容器抽象成统一节点树。

目标支持：

- Directory
- ZIP
- CAB
- 7z
- RAR
- tar / tar.gz
- ISO

每个 adapter 都需要声明：

- 是否支持 listing。
- 是否支持读取内部文件。
- 是否支持递归。
- 成本等级。
- 失败模式。
- 安全限制。

### Fingerprint Engine

生成文件或虚拟节点的指纹。

指纹不是单一 hash，而是一组层级信息：

- Metadata fingerprint
- Content hash
- Partial hash
- Archive manifest fingerprint
- Recursive tree fingerprint
- Media perceptual fingerprint
- AI summary fingerprint

不同策略选择不同指纹组合。

### Comparator

比较两个节点。

输出不是简单 true/false，而是：

- `equal`
- `similar`
- `different`
- `unknown`
- `needs_more_analysis`

每个结果必须包含：

- 命中的策略。
- 使用了哪些证据。
- 置信度。
- 下一步建议。

### Report Generator

把扫描、指纹、比较和 AI 建议汇总成专业报告。

报告是 first-class output，不依赖后续整理动作。

报告应该包含：

- 完全相等文件组。
- 高度相似文件组。
- 相似但建议保留多份的文件组。
- 建议保留的最佳版本。
- 低质量副本或冗余副本候选。
- 容器和镜像的相似性摘要。
- 例如 Windows XP 安装镜像、游戏版本包、软件安装包等推断标签。
- 每个结论的证据、置信度和风险。
- 不确定项和建议的下一步深度分析。

报告格式应该支持：

- Terminal summary
- JSON
- Markdown
- HTML

后续 GUI 可以直接消费同一份报告模型。

### Policy / Rule Engine

让用户定义相等、相似、排除、容器展开和动作策略。

规则应该支持：

- 文件类型。
- 路径模式。
- 文件大小。
- 容器类型。
- 元数据。
- 指纹结果。
- AI 建议。
- 成本预算。
- 风险等级。

### Workflow Engine

相等和相似对应不同工作流。

示例：

- 相等文件：保留一个，其他进入待删除或待归档列表。
- 相似图片：保留分辨率更高、格式更合适、修改时间更新的版本。
- 相似容器：展示差异摘要，让用户选择是否合并或保留。
- 不确定项：追加分析任务，或交给用户确认。

系统应该提供工厂模板，例如：

- Conservative Duplicate Cleanup
- Photo Quality Merge
- Archive Manifest Compare
- Deep Archive Equivalence
- ISO As Atomic
- Installer Image Review

但用户必须可以复制模板并改成自己的规则。

Workflow Engine 是可选阶段。用户可以停在报告阶段，不生成任何执行计划。

### Journal

记录实际动作。

任何真实移动、复制、删除、重命名之前都要写 journal。

journal 至少记录：

- 动作类型。
- 源路径和目标路径。
- 执行前文件指纹。
- 执行后结果。
- 时间。
- 触发的 workflow。
- 用户确认或自动规则来源。
- 回滚信息。

### Desktop Shell

桌面 shell 负责用户界面，不负责核心文件分析。

职责：

- 展示报告。
- 展示 equal/similar 分组。
- 展示风险等级和证据。
- 管理规则配置。
- 收集用户确认。
- 启动、暂停、恢复任务。

非职责：

- 不直接实现 hash 逻辑。
- 不直接实现容器遍历。
- 不直接执行删除、移动、覆盖。
- 不把浏览器权限模型作为核心文件访问方案。

Desktop Shell 与 Core Engine 的边界：

- 通过 IPC、FFI 或 sidecar process 通信。
- 所有危险动作由 core engine 执行。
- UI 只提交用户确认、配置和任务请求。
- Core engine 返回报告、进度、错误、风险等级和可执行计划。
- 通信协议必须可版本化，方便未来从 Python core 迁移到 Rust core。

## 中断恢复模型

推荐使用轻量 SQLite 或 append-only JSONL journal。

它们只承担恢复和审计作用，不承担“当前文件系统状态真相”的角色。

重启流程：

1. 读取上次未完成任务。
2. 重新 stat 相关路径。
3. 对比任务前提是否仍成立。
4. 如果成立，继续。
5. 如果变化，丢弃旧任务或降级为重新分析。
6. 如果动作已经部分完成，根据 journal 进入恢复流程。

## 成本预算

每次分析都应该有预算：

- 最大扫描文件数。
- 最大递归深度。
- 最大容器展开大小。
- 最大 hash 字节数。
- 最大运行时间。
- 最大并发数。

超出预算时，系统应该产出“需要更多分析”的结果，而不是假装已经知道答案。

## 风险等级

动作按风险分级：

- Level 0: 只读扫描。
- Level 1: 生成计划。
- Level 2: 复制文件。
- Level 3: 移动或重命名。
- Level 4: 删除、覆盖、合并。

Level 3 以上必须有 journal。

Level 4 默认需要人工确认，除非用户明确配置了自动化工作流。

## 近期实现计划

### Phase 1: 重新定义核心模型

- 引入 `NodeRef` 表示真实文件和虚拟容器节点。
- 引入 `Observation` 表示某次扫描看到的事实。
- 引入 `Fingerprint` 表示多层级指纹。
- 引入 `AnalysisTask` 表示可恢复任务。
- 引入 `ComparisonResult` 表示 equal/similar/different/unknown。
- 引入 `AnalysisReport` 表示可独立保存和阅读的专业报告。

### Phase 2: 轻量状态与恢复

- 设计 SQLite 或 JSONL journal schema。
- 实现任务队列 checkpoint。
- 实现启动时恢复流程。
- 所有动作执行前重新验证前提。

### Phase 3: 可插拔比较策略

- 实现 byte hash equality。
- 实现 metadata similarity。
- 实现 image perceptual similarity 草案。
- 实现 archive manifest similarity。
- 实现 container traversal policy。

### Phase 4: Workflow 模板

- 精确重复文件清理模板。
- 图片相似保留高质量模板。
- 压缩包清单比较模板。
- 安装镜像原子比较模板。
- 保守人工审核模板。
- 纯报告模板，不执行任何整理动作。

### Phase 5: AI 建议层

- AI 只读分析摘要。
- AI 提出 traversal policy 建议。
- AI 提出 similarity workflow 建议。
- 人类确认后才进入执行计划。

### Phase 6: 桌面产物和跨平台验证

- Python + PySide6 测试版 GUI。
- macOS `.app` 打包 spike。
- Windows `.exe` 打包 spike。
- Windows installer spike。
- macOS signing / notarization spike。
- Windows code signing spike。
- Documents、Desktop、Downloads、外接硬盘和网络盘权限策略。
- MSYS2 + zsh 开发流程验证。
- Rust core + Flutter desktop 正式版架构 spike。

## 当前原型的定位

现有 `file-organizer plan <folder>` 是一个非常早期的 CLI spike。

它可以保留作为：

- CLI 入口实验。
- dry-run 输出格式实验。
- 安全默认值实验。

但它不代表最终架构。下一步应该围绕本计划重新设计核心模型，而不是继续把扩展名分类器堆复杂。
