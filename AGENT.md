# AGENT.md

这份文档给 Codex、脚本代理和其他自动化协作者使用。项目还在早期阶段，改动时请保持小步、可验证、可解释。

## 项目定位

File Organizer 是一个证据驱动、懂用户偏好的智能文件整理高级顾问，优先级从高到低是：

1. 保护用户文件安全。
2. 不做含糊的 best effort：证据不足就说证据不足。
3. 支持随时中断、随时恢复。
4. 允许用户定义文件“相等”和“相似”的含义。
5. 把 analysis-only / report-only 当作一等产品模式。
6. 生成可解释的分析结果和整理计划。
7. 支持自定义 workflow 和可回滚执行。
8. 在稳定基础上再加入容器深度分析、AI 建议和 UI。

产品身份不是“普通 AI 文件分类器”。它是智能整理文件的高级顾问：先理解用户整理哲学，再用证据、风险、偏好和规则生成整理建议。

## 技术栈

- 当前原型：Python 3.11+、标准库优先、`src/` layout、`unittest` 测试。
- 测试版：Python CLI + Python core + PySide6 / Qt for Python GUI，可打包成 macOS `.app` 和 Windows `.exe`。
- 正式版方向：Rust core engine + Flutter desktop UI。
- 开发 shell：macOS 使用 zsh；Windows 计划使用 MSYS2 + zsh，不以 PowerShell 作为主要开发环境。

当前不要引入重量级依赖，除非它明显降低复杂度并且 README/文档同步说明原因。轻量 SQLite 或 JSONL journal 可以考虑，但不能把它设计成文件系统状态的权威缓存。

核心资产是 File Organization Runtime。AI 接口、settings、CLI、agent API 和 GUI 都是 runtime 上面的控制层，不得各自实现独立判断逻辑。

## 平台与交付

- 最终产品必须能交付 macOS `.app` 和 Windows `.exe` / installer。
- 不把浏览器或 WebView 当作默认产品路线；文件访问、扫描、hash、journal 和执行动作必须在本地桌面后端完成。
- UI shell 只负责展示、确认和配置；核心分析逻辑必须与 UI 解耦。
- UI shell 与 core engine 的边界必须明确，可以通过 IPC、FFI 或 sidecar process 通信；不要让 UI 层直接实现扫描、hash、容器遍历、journal 或删除/移动动作。
- 打包和发布必须作为产品需求处理：macOS `.app`、Windows `.exe` / installer、代码签名、macOS notarization、升级路径和崩溃日志策略都需要设计。
- 权限模型必须显式设计：访问 Documents、Desktop、Downloads、外接硬盘和网络盘前，要清楚区分只读扫描、报告导出和危险写入动作。
- Windows 开发环境按 MSYS2 + zsh 设计文档和命令，但应用必须支持原生 Windows 路径，例如 `C:\Users\...\Downloads`。
- 所有路径逻辑必须通过 `pathlib` 或目标语言的路径 API，不要手写 `/` 或 `\` 拼接。
- 不要假设文件系统大小写敏感；Windows/macOS 默认常见配置都可能大小写不敏感。
- 不要依赖 macOS-only shell 工具、路径或权限行为作为唯一实现。
- 不要把 POSIX-only 命令当作唯一开发或测试路径；Windows/MSYS2 zsh 是开发环境，但应用行为必须按跨平台本地程序设计。
- 跨平台测试需要覆盖空格路径、非 ASCII 路径、长文件名、大小写冲突和 Windows 保留名。

## 常用命令

```bash
PYTHONPATH=src python3 -m file_organizer --help
PYTHONPATH=src python3 -m file_organizer plan ~/Downloads
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m compileall src tests
```

Windows/MSYS2 zsh 也使用 zsh 风格命令；如果 Python 可执行名是 `python`，可以把上面的 `python3` 换成 `python`。

## 工作约定

- 默认实现 dry-run 或 plan 功能，避免直接改动真实用户文件。
- 用户只要专业分析报告是完全合理的完成状态，不要强行引导到执行整理。
- 不要实现 `best effort organize`。无法证明时输出 `unknown` 或 `needs_more_analysis`，需要用户偏好时请求确认。
- “懂你”必须落到可审计机制：自然语言偏好、显式 settings、review decisions、preference model 和 policy store。
- 基础用户可以用自然语言表达偏好；高级用户必须可以直接编辑精确 policy。两者最终进入同一个 runtime。
- AI 的职责是生成、解释和修正规则草案；runtime 才是判定和执行语义的权威。
- 新增执行移动文件的能力时，必须同时加入 journal、冲突处理、撤销策略和测试。
- 硬盘当前状态是唯一真相；数据库或 journal 只能用于恢复、审计和任务检查点。
- 任务设计要小粒度、幂等、可重试，支持中断后重新验证。
- 相等和相似必须通过策略表达，不要把比较逻辑写死。
- 容器文件需要 traversal policy：atomic、manifest、shallow、recursive 或 custom。
- AI 只能给建议和理由，不能直接决定删除、覆盖或合并。
- 不要在测试里操作用户主目录、Downloads、Desktop 等真实目录。
- 不要静默覆盖文件；文件名冲突必须生成唯一目标路径。
- 不要提交只适用于 macOS 的路径假设；Windows/MSYS2 zsh 是一等开发环境。
- 不要把浏览器权限模型、WebView 沙盒或 UI 选择作为文件访问设计的基础。
- 规则行为变更时，同步更新 `docs/RULES.md`。
- 用户可见行为变更时，同步更新 `README.md` 和 `docs/PRODUCT_SPEC.md`。
- 架构边界变更时，同步更新 `docs/ARCHITECTURE.md`。
- runtime、偏好学习、用户分层或产品叙事变更时，同步更新 `PLAN.md`、`docs/POSITIONING.md` 和 `docs/RUNTIME.md`。

## 代码风格

- 保持函数短小，优先使用纯函数生成计划。
- 文件系统写入集中在执行层，不要散落在分类或规则模块里。
- 错误信息应面向终端用户，可读、具体、可行动。
- 测试覆盖高风险路径：冲突、隐藏文件、递归扫描、跨平台路径。

## 仓库地图

```text
src/file_organizer/core.py      # 分类和计划生成
src/file_organizer/cli.py       # 命令行入口
tests/test_core.py              # 核心行为测试
docs/PRODUCT_SPEC.md            # 产品目标和范围
docs/POSITIONING.md             # 产品定位和用户分层
docs/RUNTIME.md                 # File Organization Runtime 设计
docs/ARCHITECTURE.md            # 模块边界和数据流
docs/ROADMAP.md                 # 阶段规划
docs/RULES.md                   # 规则系统草案
```
