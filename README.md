# 📬 Arxiv 论文每日摘要自动化系统

一个部署在 GitHub Actions 上的全自动工具，每天定时从 arXiv 抓取“里德堡原子”（可配置）相关的最新论文，并生成摘要发送到你的邮箱。

---

## ✨ 核心功能

*   **定时抓取**：每天在指定时间自动查询 arXiv。
*   **邮件推送**：将摘要结果（无论文时发送通知）发送到你的邮箱。
*   **灵活配置**：通过 `.env` 文件和 GitHub Secrets 轻松修改基本查询参数。
*   **无需运维**：基于 GitHub Actions，零服务器成本。

---

## ⚙️ 如何配置（两个关键步骤）

你的配置信息通过两种方式管理：
1.  **`.env` 文件**：用于更改检索关键词。
2.  **GitHub Secrets**：用于云端安全运行，存放敏感信息（如邮箱密码）。

### 第一步：配置 `.env` 文件（用于修改关键词和基础设置）

在项目根目录创建或修改 `.env` 文件，它是你所有配置的入口。

```ini
# ============ 【必改】Arxiv 搜索配置 ============
# 搜索关键词，用英文逗号分隔。例如，想同时监控“量子计算”和“超导”
SEARCH_KEYWORDS=Rydberg atom,Rydberg state,Rydberg excitation

# ============ 【选填】其他运行参数 ============
# 每次搜索返回的最大论文数量
MAX_RESULTS=20
```

### 第二步：配置 GitHub Secrets（用于云端运行邮箱设置）

这是让 GitHub Actions 能安全发送邮件的关键步骤。

1.  进入你的 GitHub 仓库页面。
2.  点击顶部的 **`Settings`** 选项卡。
3.  在左侧边栏找到 **`Secrets and variables`** -> **`Actions`**。
4.  点击 **`New repository secret`** 按钮，逐个添加以下三个密钥（与 `.env` 中的对应）：
    *   **`Name`**: `EMAIL_SENDER` -> `Value`: 你的QQ邮箱
    *   **`Name`**: `EMAIL_PASSWORD` -> `Value`: 你的QQ邮箱16位授权码
    *   **`Name`**: `RECIPIENT_EMAIL` -> `Value`: 收件邮箱（多个用分号 `;` 隔开）
5.  添加完成后，列表应有三项。**云端运行时，程序将优先使用这里的配置**。

---

## 🕐 如何修改发送时间

GitHub Actions 使用 **UTC 时间**（世界协调时）。你需要将期望的北京时间换算成 UTC 时间。

**换算公式**：`UTC时间 = 北京时间 - 8小时`

**示例**：
*   如果你想在 **北京时间 19:15** 发送，那么 UTC 时间是 **11:15**。
*   对应的时间表达式（Cron）为：`15 11 * * *` （表示每天UTC时间11点15分）。

**修改步骤**：
1.  在仓库中打开文件：`.github/workflows/arxiv_daily.yml`
2.  找到 `schedule` 部分，修改 `cron` 表达式的值。
    ```yaml
    on:
      schedule:
        # 修改此行：`‘分 时 * * *’` (UTC时间)
        - cron: ‘15 11 * * *’  # 例如，这代表UTC 11:15，即北京19:15
    ```
3.  保存并提交文件更改。提交后，GitHub Actions 将按新时间表运行。

---

## 🚀 开始使用

### 方法一：一键 Fork 并配置（推荐）
1.  **Fork 本仓库**到你自己的 GitHub 账户。
2.  在你 Fork 出的仓库中，按上方 **[第二步：配置 GitHub Secrets](#第二步配置-github-secrets用于云端运行邮箱设置)** 完成邮箱密钥设置。
3.  程序将在你设定的时间自动运行，可在 `Actions` 标签页查看运行状态。

### 方法二：手动运行测试
在仓库的 `Actions` 标签页，找到 **`Daily Arxiv Paper Digest`** 工作流，点击 **`Run workflow`** 按钮，可立即手动触发一次，测试配置是否正确。

---

## 📁 项目文件结构

```
arxiv-paper-digest/
├── .github/workflows/    # GitHub Actions 自动化配置
│   └── arxiv_daily.yml   # 定时任务工作流定义文件
├── main.py           # 程序主入口
├── arxiv_fetcher.py  # 论文抓取与摘要模块
├── email_sender.py   # 邮件发送模块
├── config.py             # 配置加载模块
├── .env                  # 本地配置文件（需自行创建，不上传）
├── requirements.txt      # Python 依赖列表
└── README.md             # 本说明文档
```

---

## ❓ 常见问题 (FAQ)

**Q：为什么收不到邮件？**
A：请按顺序检查：
1.  GitHub Secrets 中的邮箱和授权码（16位SMTP码）是否正确。
2.  仓库 `Actions` 页面最近一次运行日志是否有报错（红色提示）。
3.  检查邮箱的垃圾邮件文件夹。

**Q：定时任务到点没有运行？**
A：
1.  确认 `.github/workflows/arxiv_daily.yml` 文件已成功提交。
2.  GitHub Actions 的定时触发可能有几分钟延迟。

**Q：如何修改搜索的关键词？**
A：直接修改项目根目录下 `.env` 文件中的 **`SEARCH_KEYWORDS`** 变量值，用英文逗号分隔多个关键词。此修改主要影响本地运行。若需云端生效，可考虑将关键词也设为 Secret，或在代码中直接修改 `config.py`。

**Q：可以同时监控多个研究方向吗？**
A：可以。在 `SEARCH_KEYWORDS` 中用逗号添加更多关键词即可，例如：`Quantum computing, Superconductivity, Machine Learning`。

---

## 📄 许可证与AI声明

本项目由DS反复迭代约两小时完成，本项目采用 MIT 许可证。
