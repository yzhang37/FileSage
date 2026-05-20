# Contributing

感谢参与 File Organizer。这个项目处理用户文件，因此贡献时请优先考虑安全性、可预览性和可回滚性。

## 本地开发

macOS 和 Windows/MSYS2 都按 zsh 风格命令维护，不以 PowerShell 作为主要开发 shell。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests
```

Windows/MSYS2 zsh 如果使用 Windows Python，虚拟环境激活脚本可能是：

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests
```

## 提交前检查

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m compileall src tests
```

## 贡献原则

- 优先补测试，再改行为。
- File Organizer 是证据驱动、懂用户偏好的智能文件整理高级顾问，不是 best effort 文件分类器。
- AI、settings、CLI、agent API 和 GUI 都必须通过同一个 File Organization Runtime 表达判断。
- 基础用户的自然语言偏好和高级用户的精确 settings 最终都要进入可审计、可修改、可撤销的 runtime policy。
- 不确定时输出 `unknown`、`needs_more_analysis` 或 `require_confirmation`，不要伪装成确定建议。
- 所有真实文件移动能力都必须支持 dry-run。
- 不覆盖、不删除、不猜测用户意图。
- 不提交只在 macOS 或只在 MSYS2 路径语法下工作的路径逻辑。
- 路径处理使用标准路径 API，避免手写 `/` 或 `\`。
- 不把 POSIX-only 命令、浏览器权限模型或 WebView 作为核心文件访问方案。
- UI 层不得直接实现扫描、hash、容器遍历、journal 或危险文件操作；这些必须留在 core engine。
- 新增规则或分类能力时，写清楚优先级和冲突行为。
- 文档和代码一起改，避免文档漂移。

## 分支建议

```text
feature/rule-engine
feature/journal
fix/conflict-destination
docs/product-spec
```
