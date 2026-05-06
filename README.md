# File Organizer

一个面向真实工作流的高级文件夹整理程序。它的核心目标不是“把文件粗暴地搬到几个目录里”，而是先生成可解释、可回滚、可审计的整理计划，再安全地执行。

## 项目愿景

File Organizer 希望解决这些场景：

- Downloads、Desktop、项目资料夹长期堆积，文件类型和来源混杂。
- 需要按类型、时间、项目、来源、关键词或自定义规则整理文件。
- 想先预览整理结果，确认没有误判后再执行。
- 希望保留操作日志，必要时可以撤销。
- 未来可以接入重复文件检测、内容识别、AI 辅助分类和图形界面。

## 当前状态

仓库现在包含一个最小可运行的 CLI 原型：

- 扫描目标文件夹。
- 按扩展名生成整理计划。
- 默认只预览，不移动文件。
- 自动处理目标文件名冲突。
- 跳过隐藏文件，除非显式开启。

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
file-organizer plan ~/Downloads
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
- 计划必须可解释：每个目标路径都要能说明来自哪条规则。
- 文件操作必须可回滚：执行阶段需要写入 journal。
- 规则系统优先确定性，AI 分类只能作为可审核建议。
- 对用户文件保持保守：不猜测、不静默覆盖、不隐藏错误。

## 文档

- [产品规格](docs/PRODUCT_SPEC.md)
- [架构说明](docs/ARCHITECTURE.md)
- [路线图](docs/ROADMAP.md)
- [规则系统草案](docs/RULES.md)
- [协作指南](CONTRIBUTING.md)

