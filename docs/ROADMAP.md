# Roadmap

## Phase 0: Repository Foundation

- [x] 初始化 Git 仓库。
- [x] 添加 README、AGENT、贡献指南和基础文档。
- [x] 添加最小 CLI 原型。
- [x] 添加核心测试。

## Phase 1: Planning Engine

- [ ] 重新定义核心模型：`NodeRef`、`Observation`、`Fingerprint`、`AnalysisTask`、`ComparisonResult`。
- [ ] 明确硬盘是真相，轻量状态只做 journal/checkpoint。
- [ ] 设计可中断、可恢复任务队列。
- [ ] 设计分析成本预算。
- [ ] 设计 `AnalysisReport` 模型。
- [ ] 设计 UI shell / core engine 边界和 IPC/FFI/sidecar 通信模型。
- [ ] 保留当前扩展名分类 CLI 作为 spike，不继续围绕它堆复杂逻辑。

## Phase 2: Equality / Similarity Engine

- [ ] 实现 byte hash equality。
- [ ] 实现 metadata similarity。
- [ ] 实现用户可定义 equal/similar 策略。
- [ ] 输出证据、置信度和 `needs_more_analysis`。
- [ ] 扩展比较策略测试矩阵。

## Phase 3: Container / Virtual Filesystem

- [ ] 设计 virtual node graph。
- [ ] 实现 directory adapter。
- [ ] 实现 ZIP manifest adapter。
- [ ] 实现 tar manifest adapter。
- [ ] 设计 CAB、7z、RAR、ISO adapter 边界。
- [ ] 实现 atomic、manifest、shallow、recursive traversal policy。

## Phase 4: Safe Execution

前置要求：报告和 dry-run 计划已经足够可解释。用户可以停留在报告阶段，不执行任何动作。

- [ ] 设计 journal 格式。
- [ ] 实现移动执行器。
- [ ] 实现撤销命令。
- [ ] 支持失败恢复。
- [ ] 添加跨平台文件系统测试。

## Phase 5: Advanced Classification

- [ ] 重复文件检测。
- [ ] 内容哈希。
- [ ] 文件元数据读取。
- [ ] 文档和图片内容摘要。
- [ ] AI 辅助分类建议。

## Phase 6: User Experience

- [ ] 专业分析报告的终端视图。
- [ ] Markdown、JSON、HTML 报告导出。
- [ ] 交互式终端确认。
- [ ] Python + PySide6 图形界面原型。
- [ ] 规则调试器。
- [ ] 计划预览和筛选。
- [ ] 定时整理。

## Phase 7: Desktop Delivery

- [ ] 验证 Windows/MSYS2 + zsh 开发流程。
- [ ] 添加跨平台路径测试：空格、非 ASCII、大小写冲突、Windows 保留名、长路径。
- [ ] macOS `.app` 打包 spike。
- [ ] Windows `.exe` 打包 spike。
- [ ] Windows installer spike。
- [ ] macOS signing / notarization spike。
- [ ] Windows code signing spike。
- [ ] Documents、Desktop、Downloads、外接硬盘和网络盘权限模型 spike。
- [ ] 评估签名、notarization 和 installer 流程。
- [ ] Rust core + Flutter desktop 正式版架构 spike。
