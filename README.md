🧰 TDL 图形化命令生成器 — Telegram 下载与导出辅助工具（Python GUI） 想下载 Telegram 媒体、导出频道消息或生成复杂的 TDL 命令，却被命令行折腾得头疼？这套基于 Python 图形界面（GUI）开发的 TDL 辅助工具合集，可以让你轻松通过可视化界面生成完整的 TDL 命令，只需复制命令到 CMD、PowerShell 或终端中运行即可完成下载或导出。

💡 项目简介

本项目是 iyear/tdl 的辅助工具集合，使用 Python 编写，专为想使用 TDL 却不熟悉命令行的用户设计。这些脚本不会直接下载 Telegram 内容，而是帮助用户可视化生成 TDL 命令，从而大幅降低使用门槛。生成命令后，复制到命令行中执行即可。所有脚本均由 AI（ChatGPT）辅助生成，并严格参考 TDL 官方文档，覆盖了大部分核心功能，让普通用户也能轻松理解和使用。

📦 工具合集概览

该项目包含三个独立的 Python GUI 工具，分别用于不同场景的命令生成。三个脚本运行方式完全相同：进入对应文件夹 → 运行 main.py 文件。

📂 1. 单链接多链接下载

用于根据 Telegram 的消息或帖子链接生成下载命令。可同时处理单个或多个链接，支持自动拼接命令参数，一键生成 tdl dl 命令。非常适合希望按链接批量下载媒体资源的用户。运行方式：进入「单链接多链接下载」文件夹，运行 main.py。

📁 2. 群或频道下载

用于构建针对 Telegram 群组或频道的批量下载命令。支持反序下载 (–desc)、自动跳过重复文件 (–skip-same)、群组组合下载 (–group)、MIME 修正扩展名 (–rewrite-ext)。界面中可自由设置线程数、并发参数、输出目录等选项。适合按频道或群组进行大批量下载的用户。运行方式：进入「群或频道下载」文件夹，运行 main.py。

📊 3. 导出 JSON（带筛选功能）

用于将 Telegram 聊天记录、媒体消息导出为 JSON 文件。支持按消息内容或文件名筛选（Message contains、Media.Name contains）、按浏览量、转发数或文件大小筛选、按发送者 ID 限定导出范围、按时间戳或消息 ID 范围导出（-T / -i 参数），并支持附加参数 –with-content、–raw、–all 等。非常适合数据归档、日志分析、自动化备份等场景。运行方式：进入「导出 Json 带筛选功能」文件夹，运行 main.py。

🚀 使用步骤
	1.	安装 Python 3.9+（自带 tkinter 模块）
	2.	安装并配置 TDL（执行下载或导出命令所需）
	3.	下载或克隆本项目：git clone https://github.com/你的用户名/你的仓库名.git
	4.	进入任意功能文件夹并运行 main.py：cd 单链接多链接下载 → python main.py
	5.	在图形界面中填写链接、筛选条件或导出范围
	6.	点击 “生成命令” → “复制命令”
	7.	打开 CMD / PowerShell / Terminal，粘贴命令执行

⚠️ 注意：这些脚本不会直接执行下载或导出操作，它们只用于生成命令。真正执行命令仍需已安装并配置好的 TDL 环境。

📘 示例命令

以下为 GUI 自动生成的 TDL 命令示例：
导出包含“项目”关键字的消息：tdl chat export -c https://t.me/example -o "tdl-export.json" -f "Message contains '项目'"
下载 Telegram 频道中所有 zip 文件：tdl dl -c https://t.me/example -f "Media.Name endsWith '.zip'"

🧠 设计理念

原版 TDL 是一款功能强大的 Telegram 下载器，但命令行参数众多、语法复杂。本项目旨在让命令行变得简单可视化，通过 GUI 实现：✅ 自动拼接参数，防止语法错误 ✅ 提供输入框、下拉菜单、复选框来直观配置参数 ✅ 一键生成可直接执行的命令 ✅ 适合学习 TDL 命令语法的新用户

📁 项目结构

📁 TDL GUI Helper Tools
├── 单链接多链接下载/（main.py, ui_main.py, command_builder.py, utils.py, validators.py）
├── 群或频道下载/（main.py, ui_main.py, template_config.py, command_builder.py, sanitizer.py, utils.py）
├── 导出 Json 带筛选功能/（main.py, gui_main.py, tdl_logic.py, utils.py）
└── README.md

所有脚本运行方式一致：进入对应文件夹 → 运行 main.py 即可。

🧩 功能特性一览
	•	图形化命令生成（无需记忆命令行）
	•	支持多类型任务：链接下载 / 群组下载 / JSON 导出
	•	提供关键词筛选、浏览数过滤、文件大小筛选
	•	支持附加参数（–with-content、–raw、–all）
	•	自动生成命名模板（–template）
	•	检测非法字符，防止保存出错
	•	跨平台支持（Windows / macOS / Linux）
	•	全部基于 Python 标准库，无需额外依赖

⚙️ 环境要求
	•	Python 3.9 或更高版本
	•	已安装 TDL CLI 工具
	•	操作系统兼容：Windows / macOS / Linux
	•	无需第三方库，开箱即用

📗 文档与参考资料
	•	官方仓库：https://github.com/iyear/tdl
	•	官方文档：https://docs.iyear.me/tdl/
	•	所有命令参考 TDL 官方语法
	•	三个脚本覆盖核心功能，但不保证包含全部参数

🔒 免责声明
	•	本项目仅用于生成命令，不提供直接下载或导出功能
	•	运行需已安装并配置好 TDL
	•	不与 Telegram 官方 API 通信，不保存任何数据
	•	使用者需遵守相关法规
	•	作者不承担任何使用风险

🧑‍💻 开发说明
	•	开发语言：Python
	•	界面框架：Tkinter
	•	AI 辅助开发（ChatGPT）
	•	参考官方文档规范
	•	目标：让每个人都能轻松使用 TDL

💬 作者寄语

“让命令行工具更容易被所有人使用。” 这套 GUI 工具让 TDL 的强大功能变得直观简单。无论技术用户还是普通用户，都能轻松生成命令、完成下载与导出。如果本项目对你有帮助，欢迎 Star 支持或提交改进建议。

⭐ 支持项目

如果你喜欢本项目，请为它点亮 Star 🌟，让更多人发现这款高效的 Telegram 命令生成器。

© 2025 TDL GUI Helper Tools — Powered by Python & ChatGPT

<img width="1761" height="761" alt="wechat_2025-10-15_221944_092" src="https://github.com/user-attachments/assets/e2d3f134-011f-4293-afe6-e5e733040631" />
<img width="1321" height="852" alt="wechat_2025-10-15_221831_079" src="https://github.com/user-attachments/assets/b4bb0756-0b5d-4132-9936-700322050de4" />
<img width="951" height="731" alt="wechat_2025-10-15_221716_819" src="https://github.com/user-attachments/assets/9bb45fc7-c784-4a18-b355-83179ee3d9df" />
