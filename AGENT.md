# AGENT.md

这份文档给 Codex、脚本代理和其他自动化协作者使用。项目还在早期阶段，改动时请保持小步、可验证、可解释。

## 项目定位

File Organizer 是一个高级文件夹整理程序，优先级从高到低是：

1. 保护用户文件安全。
2. 生成可解释的整理计划。
3. 支持自定义规则和可回滚执行。
4. 在稳定基础上再加入智能分类、重复文件检测和 UI。

## 技术栈

- Python 3.11+
- 标准库优先
- `src/` layout
- `unittest` 测试

当前不要引入重量级依赖，除非它明显降低复杂度并且 README/文档同步说明原因。

## 常用命令

```bash
PYTHONPATH=src python3 -m file_organizer --help
PYTHONPATH=src python3 -m file_organizer plan ~/Downloads
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m compileall src tests
```

## 工作约定

- 默认实现 dry-run 或 plan 功能，避免直接改动真实用户文件。
- 新增执行移动文件的能力时，必须同时加入 journal、冲突处理、撤销策略和测试。
- 不要在测试里操作用户主目录、Downloads、Desktop 等真实目录。
- 不要静默覆盖文件；文件名冲突必须生成唯一目标路径。
- 规则行为变更时，同步更新 `docs/RULES.md`。
- 用户可见行为变更时，同步更新 `README.md` 和 `docs/PRODUCT_SPEC.md`。
- 架构边界变更时，同步更新 `docs/ARCHITECTURE.md`。

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
docs/ARCHITECTURE.md            # 模块边界和数据流
docs/ROADMAP.md                 # 阶段规划
docs/RULES.md                   # 规则系统草案
```

