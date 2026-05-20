# File Organizer

一个面向真实工作流的高级文件夹整理程序。它的核心目标不是“把文件粗暴地搬到几个目录里”，而是帮助用户安全地分析、比较、去重、归档和整理复杂文件集合。

更完整的产品设想见 [PLAN.md](PLAN.md)。

## 项目愿景

File Organizer 希望解决这些场景：

- Downloads、Desktop、项目资料夹长期堆积，文件类型和来源混杂。
- 需要按类型、时间、项目、来源、关键词或自定义规则整理文件。
- 需要识别相等文件、相似文件、不同格式的重复内容和复杂容器文件。
- 希望处理 ZIP、CAB、7z、RAR、ISO 等嵌套内容，但又不想无脑展开所有文件。
- 任务可能很重，需要随时中断、随时恢复。
- 只想运行 DryRun，得到专业报告，然后自己决定如何处理。
- 最终需要真正的桌面产物：macOS `.app` 和 Windows `.exe` / installer。
- 想先预览整理结果，确认没有误判后再执行。
- 希望保留操作日志，必要时可以撤销。
- 未来可以接入内容识别、AI 辅助策略建议和图形界面。

## 当前状态

仓库现在包含一个最小可运行的 CLI 原型。它只是早期 spike，不代表最终架构：

- 扫描目标文件夹。
- 按扩展名生成整理计划。
- 默认只预览，不移动文件。
- 自动处理目标文件名冲突。
- 跳过隐藏文件，除非显式开启。

## 技术路线

- 当前原型：Python CLI，优先跑通安全模型、报告模型和核心分析概念。
- 测试版：Python CLI + Python core + PySide6 / Qt for Python GUI，打包为 macOS `.app` 和 Windows `.exe`。
- 正式版方向：Rust core engine + Flutter desktop UI。
- Windows 开发环境：MSYS2 + zsh，不以 PowerShell 作为主要开发 shell。
- 产品路线：不默认使用浏览器或 WebView；核心文件访问、扫描、hash、journal 和执行动作都应在本地桌面后端完成。
- UI 与核心分析逻辑解耦：桌面 shell 通过 IPC、FFI 或 sidecar process 调用 core engine。
- 发布工程是一等需求：`.app`、`.exe`、installer、签名、macOS notarization 和用户目录权限模型都需要进入设计。

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
file-organizer plan ~/Downloads
```

在 Windows/MSYS2 zsh 中也使用 zsh 风格命令。如果使用 Windows Python，虚拟环境激活脚本可能位于 `.venv/Scripts/activate`：

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e .
file-organizer plan /c/Users/<you>/Downloads
```

不安装也可以直接运行：

```bash
PYTHONPATH=src python3 -m file_organizer plan ~/Downloads
```

运行测试：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## 示例

```bash
file-organizer plan ~/Downloads --recursive
file-organizer plan ~/Downloads --json
file-organizer plan ~/Downloads --include-hidden
```

输出中的每一行都是一条计划，不会真实移动文件：

```text
~/Downloads/report.pdf -> ~/Downloads/Documents/report.pdf
~/Downloads/photo.jpg -> ~/Downloads/Images/photo.jpg
```

## 项目结构

```text
.
├── AGENT.md                  # 给 AI/自动化协作者的工作约定
├── AGENTS.md                 # 兼容部分工具的代理说明入口
├── PLAN.md                   # 核心产品和架构计划
├── README.md                 # 项目介绍和快速开始
├── CONTRIBUTING.md           # 贡献指南
├── docs/
│   ├── ARCHITECTURE.md       # 架构说明
│   ├── PRODUCT_SPEC.md       # 产品规格
│   ├── ROADMAP.md            # 路线图
│   └── RULES.md              # 规则系统草案
├── src/file_organizer/       # 应用源码
└── tests/                    # 测试
```

## 设计原则

- 默认 dry-run，任何移动或删除都必须明确确认。
- Analysis-only / report-only 是一等模式，不是整理流程的附属功能。
- 计划必须可解释：每个目标路径都要能说明来自哪条规则。
- 文件操作必须可回滚：执行阶段必须写入 journal。
- 硬盘当前状态是唯一真相，轻量数据库只做任务恢复和审计。
- 支持用户定义“相等”和“相似”，不要把比较逻辑写死。
- 容器文件可以被展开，也可以被当作原子文件，取决于策略。
- AI 只能作为可审核建议，不能直接承担删除、覆盖、合并责任。
- 对用户文件保持保守：不猜测、不静默覆盖、不隐藏错误。
- 跨平台是一等约束：macOS 和 Windows 都必须可开发、可测试、可打包。
- 访问 Documents、Desktop、Downloads、外接硬盘和网络盘时，必须明确权限、风险等级和用户确认方式。

## 文档

- [核心计划](PLAN.md)
- [产品规格](docs/PRODUCT_SPEC.md)
- [架构说明](docs/ARCHITECTURE.md)
- [路线图](docs/ROADMAP.md)
- [规则系统草案](docs/RULES.md)
- [协作指南](CONTRIBUTING.md)
