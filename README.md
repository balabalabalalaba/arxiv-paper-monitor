# 📬 Arxiv 论文每日摘要自动化系统

一个部署在 GitHub Actions 上的全自动工具，每天定时从 arXiv 抓取你自定义的研究关键词相关的最新论文，并生成摘要发送到你的邮箱。

---

## ✨ 核心功能

*   **定时抓取**：每天在指定时间自动查询 arXiv。
*   **邮件推送**：将摘要结果（无论文时也会发送通知）发送到你的邮箱。
*   **灵活配置**：通过 GitHub Variables 和 GitHub Secrets 轻松修改关键词、搜索范围和邮箱信息。
*   **无需运维**：基于 GitHub Actions，零服务器成本。

---

## 🚀 开始使用（三步上手）

### 第一步：Fork 本仓库

点击页面右上角的 **`Fork`** 按钮，将本仓库复制到你自己的 GitHub 账户下。

后续所有配置都在你 Fork 出的仓库中进行。

### 第二步：配置搜索参数（GitHub Variables）

这里设置你想监控的关键词、查找天数和返回数量。**不需要改任何代码文件。**

1.  进入你 Fork 的仓库，点击顶部 **`Settings`** 选项卡。
2.  左侧边栏找到 **`Secrets and variables`** → **`Actions`**。
3.  点击 **`Variables`** 标签页（注意：不是 Secrets 那个标签）。
4.  点击 **`New repository variable`**，逐个添加以下参数：

| Name | 说明 | 示例值 |
|------|------|--------|
| `SEARCH_KEYWORDS` | 搜索关键词，英文逗号分隔 | `quantum computing,superconductivity` |
| `SEARCH_CATEGORIES` | 只在指定 arXiv 分区搜索，逗号分隔，**留空表示不限制** | `physics.atom-ph,quant-ph,physics.optics` |
| `FETCH_DAYS` | 查找过去几天的论文（默认 2） | `2` |
| `MAX_RESULTS` | 每次最多返回几篇论文（默认 20） | `20` |

> **提示**：`SEARCH_KEYWORDS` 请用英文关键词，arXiv 为英文数据库。常用分区代码：`quant-ph`（量子物理）、`physics.atom-ph`（原子物理）、`physics.optics`（光学）、`cond-mat`（凝聚态）、`cs.AI`（人工智能）。完整列表见 [arxiv.org/category_taxonomy](https://arxiv.org/category_taxonomy)。

### 第三步：配置邮箱（GitHub Secrets）

这里存放邮箱账号和密码等敏感信息。

1.  同样在 **`Settings`** → **`Secrets and variables`** → **`Actions`** 下，切换到 **`Secrets`** 标签页。
2.  点击 **`New repository secret`**，逐个添加以下三个密钥：

| Name | 说明 |
|------|------|
| `EMAIL_SENDER` | 你的发件邮箱（支持 QQ 邮箱、163 邮箱） |
| `EMAIL_PASSWORD` | 邮箱 SMTP 授权码（**不是登录密码**，见下方说明） |
| `RECIPIENT_EMAIL` | 收件邮箱，多个收件人用分号 `;` 隔开 |

**如何获取 QQ 邮箱 SMTP 授权码：**
1.  登录 QQ 邮箱网页版 → **设置** → **账户**。
2.  找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"，开启 **SMTP 服务**。
3.  按提示验证手机后，会生成一个 **16 位授权码**，将它填入 `EMAIL_PASSWORD`。

> **提示**：`RECIPIENT_EMAIL` 可以填任意邮箱，不必和发件箱相同。

---

## 🕐 如何修改发送时间

GitHub Actions 使用 **UTC 时间**（世界协调时）。

**换算公式**：`UTC 时间 = 北京时间 - 8 小时`

**示例**：
*   想在 **北京时间 09:00** 发送 → UTC 时间 **01:00** → cron 表达式 `0 1 * * *`
*   想在 **北京时间 19:15** 发送 → UTC 时间 **11:15** → cron 表达式 `15 11 * * *`

**修改步骤**：
1.  在仓库中打开文件：`.github/workflows/arxiv_daily.yml`
2.  找到 `schedule` 部分，修改 `cron` 表达式。
    ```yaml
    on:
      schedule:
        # 格式：'分 时 * * *'（UTC 时间）
        - cron: '0 1 * * *'  # UTC 01:00 = 北京 09:00
    ```
3.  保存并提交文件，GitHub Actions 将按新时间运行。

---

## 🔍 如何修改搜索关键词

**云端运行（推荐）**：回到上方 [第二步：配置 GitHub Variables](#第二步配置搜索参数github-variables)，直接在网页上修改 `SEARCH_KEYWORDS` 的值，无需改任何代码。

**本地运行**：修改项目根目录下的 `.env` 文件：
```ini
SEARCH_KEYWORDS=量子计算,超导,机器学习
FETCH_DAYS=2
MAX_RESULTS=20
```

---

## ▶️ 手动触发测试

配置完成后，可以立即手动运行一次来验证配置是否正确：

在仓库的 **`Actions`** 标签页，找到 **`Daily Arxiv Paper Digest`** 工作流，点击 **`Run workflow`** 按钮。

几分钟后检查你的收件箱（也检查一下垃圾邮件文件夹）。

---

## 📁 项目文件结构

```
arxiv-paper-monitor/
├── .github/workflows/    # GitHub Actions 自动化配置
│   └── arxiv_daily.yml   # 定时任务工作流定义文件
├── main.py               # 程序主入口
├── arxiv_fetcher.py      # 论文抓取与摘要模块
├── email_sender.py       # 邮件发送模块
├── config.py             # 配置加载模块
├── .env                  # 本地运行配置文件（不提交到 GitHub）
├── requirements.txt      # Python 依赖列表
└── README.md             # 本说明文档
```

---

## ❓ 常见问题 (FAQ)

**Q：为什么收不到邮件？**
A：请按顺序检查：
1.  GitHub Secrets 中的 `EMAIL_SENDER` 和 `EMAIL_PASSWORD`（16 位 SMTP 授权码）是否填写正确。
2.  仓库 `Actions` 页面最近一次运行日志是否有报错（红色提示）。
3.  检查收件箱的**垃圾邮件**文件夹。

**Q：如何修改搜索关键词？**
A：进入 `Settings → Secrets and variables → Actions → Variables` 标签页，修改 `SEARCH_KEYWORDS` 的值。**不需要改任何代码文件。**

**Q：`FETCH_DAYS` 和 `MAX_RESULTS` 怎么设置？**
A：同样在 GitHub Variables 里添加或修改对应的变量值。`FETCH_DAYS` 建议设为 `1`（只看昨天）或 `2`（看最近两天），`MAX_RESULTS` 设为 `20`~`50` 即可。

**Q：如何只搜索特定 arXiv 分区？**
A：在 GitHub Variables 里添加 `SEARCH_CATEGORIES`，填入分区代码（逗号分隔），例如 `physics.atom-ph,quant-ph,physics.optics`。不设置此变量则搜索全部分区。分区代码见 [arxiv.org/category_taxonomy](https://arxiv.org/category_taxonomy)。

**Q：定时任务到点没有运行？**
A：
1.  确认 `.github/workflows/arxiv_daily.yml` 文件已成功提交。
2.  GitHub Actions 的定时触发可能有几分钟甚至更长的延迟，属于正常现象。

**Q：可以同时监控多个研究方向吗？**
A：可以。在 `SEARCH_KEYWORDS` 中用英文逗号添加更多关键词，例如：`quantum computing, superconductivity, machine learning, topological insulator`。

**Q：支持哪些邮箱？**
A：目前支持 QQ 邮箱（smtp.qq.com）和 163 邮箱（smtp.163.com）。其他支持 SMTP 的邮箱也可以使用，但可能需要修改 `email_sender.py` 中的服务器地址。

---

## 📄 许可证与说明

本项目由 DS 反复迭代约两小时完成，几乎全 AI 生成，包括本文档。作者只负责检查代码可运行性。项目最初在本地部署，部分功能仅在本地运行时有效，如有让人困惑的方法或函数，可忽略或让 AI 协助理解。

本项目采用 **MIT 许可证**，欢迎自由使用和修改。
