# File Organizer

File Organizer 是一个证据驱动、懂用户偏好的智能文件整理高级顾问。它不是“AI 猜一个分类然后 best effort 搬文件”，而是先理解你的判断标准，分析文件关系，解释证据和风险，再生成可审核、可回滚、可交给 AI agent 执行的整理方案。

给普通用户的一句话：

> AI 整理文件前，先帮你的文件夹做一次安全体检。看清哪些真的重复，哪些只是相似，哪些不能乱动，然后再安全整理。

更完整的产品设想见 [PLAN.md](PLAN.md)。

## 项目愿景

File Organizer 希望解决这些场景：

- Downloads、Desktop、项目资料夹长期堆积，文件类型和来源混杂。
- 需要一个懂自己整理习惯的 AI 高级顾问，而不是含糊的自动分类器。
- 需要识别相等文件、相似文件、不同格式的重复内容和复杂容器文件。
- 希望处理 ZIP、CAB、7z、RAR、ISO 等嵌套内容，但又不想无脑展开所有文件。
- 任务可能很重，需要随时中断、随时恢复。
- 只想运行 DryRun，得到专业报告，然后自己决定如何处理。
- 最终需要真正的桌面产物：macOS `.app` 和 Windows `.exe` / installer。
- 想先预览整理结果，确认没有误判后再执行。
- 希望保留操作日志，必要时可以撤销。
- 未来可以接入内容识别、AI 辅助策略建议和图形界面。

## 产品分层

- 基础用户：用自然语言讲清楚整理偏好，AI 生成可见、可改、可撤销的规则草案。
- 高级用户：直接在 settings 中配置 equal/similar/traversal/risk/workflow 等精确规则。
- 专家和 AI agent：通过 CLI / JSON / API 调用 `analyze`、`compare`、`report`、`safe-plan`。

三层入口共享同一个 File Organization Runtime。AI 接口和精确 settings 都只是运行时之上的控制层。

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
- 核心资产：File Organization Runtime，负责 equal/similar/unknown/needs_more_analysis、policy、evidence、risk、report、safe-plan 和 journal。

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
│   ├── POSITIONING.md        # 产品定位和用户分层
│   ├── PRODUCT_SPEC.md       # 产品规格
│   ├── ROADMAP.md            # 路线图
│   ├── RUNTIME.md            # File Organization Runtime 设计
│   └── RULES.md              # 规则系统草案
├── src/file_organizer/       # 应用源码
└── tests/                    # 测试
```

## 设计原则

- 这是智能文件整理，但必须是证据驱动、懂用户偏好的整理。
- 不做含糊的 best effort：证据不足就输出 `unknown` 或 `needs_more_analysis`。
- 默认 dry-run，任何移动或删除都必须明确确认。
- Analysis-only / report-only 是一等模式，不是整理流程的附属功能。
- 计划必须可解释：每个目标路径都要能说明来自哪条规则。
- 文件操作必须可回滚：执行阶段必须写入 journal。
- 硬盘当前状态是唯一真相，轻量数据库只做任务恢复和审计。
- 支持用户定义“相等”和“相似”，不要把比较逻辑写死。
- 支持两层“懂你”：自然语言偏好输入和高级 settings 精确配置。
- 容器文件可以被展开，也可以被当作原子文件，取决于策略。
- AI 只能作为可审核建议，不能直接承担删除、覆盖、合并责任。
- 对用户文件保持保守：不猜测、不静默覆盖、不隐藏错误。
- 跨平台是一等约束：macOS 和 Windows 都必须可开发、可测试、可打包。
- 访问 Documents、Desktop、Downloads、外接硬盘和网络盘时，必须明确权限、风险等级和用户确认方式。

## 文档

- [核心计划](PLAN.md)
- [产品定位](docs/POSITIONING.md)
- [运行时架构](docs/RUNTIME.md)
- [产品规格](docs/PRODUCT_SPEC.md)
- [架构说明](docs/ARCHITECTURE.md)
- [路线图](docs/ROADMAP.md)
- [规则系统草案](docs/RULES.md)
- [协作指南](CONTRIBUTING.md)
