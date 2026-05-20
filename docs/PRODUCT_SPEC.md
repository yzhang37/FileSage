# Product Spec

## 一句话说明

FileSage 是一个证据驱动、懂用户偏好的智能文件整理高级顾问：它允许用户用自然语言或精确 settings 定义文件“相等”和“相似”的含义，渐进式分析普通文件、目录和嵌套容器，既可以只生成专业分析报告，也可以进一步生成可审核、可恢复、可回滚的整理工作流。

最终产品必须是可安装/可运行的桌面应用：macOS `.app` 和 Windows `.exe` / installer。

## 目标用户

- 经常整理 Downloads、Desktop、截图、文档归档的个人用户。
- 希望 AI 听懂自己整理习惯，而不是只做通用分类的基础用户。
- 需要把资料按项目、来源、时间、质量或关系归档的知识工作者。
- 希望批量整理但担心误删、覆盖、误移动的谨慎用户。
- 需要比较图片、压缩包、安装镜像和多版本资料集的高级用户。
- 只想看专业报告，然后自己手动决定处理方式的用户。
- 希望在 Windows 和 macOS 上使用同一套核心能力的用户。
- 希望通过 CLI / JSON / API 调用文件关系分析能力的 AI agent 和 developer。

## 核心问题

普通整理脚本通常有这些风险：

- 规则不可见，用户不知道文件为什么会被移动。
- 执行不可撤销，出错后很难恢复。
- 冲突处理粗糙，容易覆盖文件或制造混乱。
- 只按路径和扩展名分类，无法表达“内容相等”或“内容相似”。
- 把数据库当作文件系统缓存，状态很快过期。
- 对 ZIP、ISO 等容器要么完全无视，要么成本失控地全部展开。

FileSage 的产品策略是：硬盘当前状态永远是事实来源，系统只用轻量状态记录任务进度、journal 和审计线索。分析结果必须可解释，执行动作必须可回滚。

DryRun / analysis-only 是核心产品模式。用户可以只要报告，不让程序执行任何整理动作。

桌面产品不默认走浏览器/WebView 权限路线。文件系统访问、扫描、指纹、journal 和执行动作必须由本地 core engine 负责。

桌面 UI 只是 shell。它通过 IPC、FFI 或 sidecar process 调用 core engine，不直接实现扫描、hash、容器遍历、journal 或危险文件操作。

File Organization Runtime 是核心资产。AI advisor、advanced settings、CLI / JSON / Agent API 和桌面 GUI 都是 runtime 之上的控制层。

系统不做含糊的 best effort。如果证据不足，输出 `unknown` 或 `needs_more_analysis`；如果风险高，输出 `require_confirmation`；如果需要用户偏好，就停下来问。

## MVP 范围

- 定义核心数据模型：真实文件节点、虚拟容器节点、观察结果、指纹、分析任务和比较结果。
- 定义 File Organization Runtime：policy、predicate、evidence、risk、report、safe-plan、journal。
- 定义 Preference Model 和 Review Decision Store，用于记录用户判断标准，不作为文件系统状态 cache。
- 支持可中断、可恢复的只读扫描任务。
- 实现轻量 journal/checkpoint，不把数据库当作权威缓存。
- 实现 byte hash 相等策略。
- 实现基础 metadata 相似策略。
- 生成专业分析报告：完全相等组、高度相似组、建议保留项、不确定项。
- 生成 dry-run 计划，不移动、不删除文件。
- 输出 agent-friendly JSON。
- 明确跨平台路径模型，支持 macOS 和 Windows/MSYS2 zsh 开发流程。
- 明确 UI shell / core engine 边界和通信方式。
- 保留当前扩展名分类 CLI 作为早期 spike。

## V1 范围

- 规则配置文件。
- 用户可定义相等/相似策略。
- 自然语言偏好输入生成规则草案。
- 高级 settings 直接编辑 runtime policy。
- review decisions 本地学习和可撤销偏好管理。
- 操作 journal 和撤销。
- 安全执行移动、复制、归档。
- 容器 traversal policy：atomic、manifest、shallow、recursive、custom。
- ZIP 和 tar manifest 分析。
- 重复文件和相似文件分组。
- Markdown、JSON、HTML 报告导出。
- 工作流模板。
- Python + PySide6 测试版桌面 GUI。
- macOS `.app` 和 Windows `.exe` 打包 spike。
- Windows installer、macOS signing / notarization、Windows code signing spike。
- Documents、Desktop、Downloads、外接硬盘和网络盘权限模型。

## V2 方向

- CAB、7z、RAR、ISO adapter。
- 图片感知哈希和质量保留策略。
- 内容摘要和语义分类建议。
- AI 辅助排除项、容器策略和工作流建议。
- Rust core engine + Flutter desktop UI。
- 正式 macOS `.app`、Windows `.exe` / installer、签名和发布流程。
- 规则调试器。
- 计划差异视图。
- 定时整理和后台监控。

## 非目标

- 不做危险的一键删除。
- 不默认上传用户文件。
- 不在没有 journal 的情况下批量移动。
- 不默认接管系统文件夹。
- 不默认深度展开所有容器文件。
- 不让 AI 自动决定删除、覆盖或合并。

## 成功标准

- 用户能在执行前清楚看到每个文件的目标位置。
- 用户能感觉系统越来越懂自己的整理习惯，但所有“懂你”都可查看、可编辑、可撤销。
- 用户可以只阅读报告并手动处理，不必进入整理流程。
- 同名文件不会被覆盖。
- 所有执行动作可以从 journal 追溯。
- 中断后重启可以安全继续或重新分析。
- 用户可以清楚定义相等和相似的含义。
- 每个建议都能引用证据、runtime policy 和用户偏好来源。
- 不确定时不会装懂，会输出 `unknown` / `needs_more_analysis` / `require_confirmation`。
- AI agent 可以消费稳定 JSON 输出，而不是自己猜文件关系。
- 常见整理任务可以通过 workflow 模板复用。
- 错误信息能帮助用户修复问题，而不是只显示堆栈。
