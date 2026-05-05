# implement-doc Codex 工作流

本目录可以作为 `.codex` home 使用，里面安装了 `implement-doc` 工作流。

这个工作流会把 roadmap、实现文档、SPEC、TODO 计划等文档转换成一个可审计的 Codex 实现流程：

- 当前 Codex 会话是 controller，负责保护 roadmap 和上下文；
- 只有一个持久化 Codex MCP worker 负责真正写代码；
- worker prompt、状态、报告、incident、decision、notification 都会落盘；
- Resend 用于正式邮件通知和长报告投递；
- Telegram 用于短通知和可执行的远程纯文本回复；
- Signal 默认禁用。

## 已安装目录

当前目录包含：

```text
config.toml
prompts/
  implement-doc.md
skills/
  implement-doc/
    SKILL.md
    assets/
    references/
    scripts/
roadmap.md
```

当工作流在某个项目 repo 里运行时，会在该项目里生成运行时产物：

```text
.codex-orchestrator/
  implement-doc/
    state/
    reports/
    incidents/
    prompts/
    decisions/
    remote-decisions/
    notifications/
```

运行时 state 文件是该 run 的事实来源，里面保存 run ID、roadmap 路径、worker thread ID、通知配置和待处理远程决策。

## 所需工具链

需要以下命令可用：

```bash
python3
node
npm
npx
codex
git
timeout
```

MCP server 配置在 `config.toml` 中：

```toml
[mcp_servers.codex_worker]
command = "codex"
args = ["mcp-server"]

[mcp_servers.telegram_notifier]
command = "npx"
args = ["-y", "telegram-notifier-mcp"]

[mcp_servers.resend]
command = "npx"
args = ["-y", "resend-mcp"]
```

## 部署方式

你可以直接把当前目录作为 Codex home：

```bash
export CODEX_HOME=/home/kunorikiku/source/codex-workflow-deploy
```

也可以把本目录内容复制到默认 Codex home，通常是：

```text
~/.codex/
```

部署后检查 Codex 是否能读到 MCP 配置：

```bash
CODEX_HOME=/home/kunorikiku/source/codex-workflow-deploy codex mcp list
```

应能看到：

```text
codex_worker
resend
telegram_notifier
```

## 必须填写的位置

有两个配置入口：

- `config.toml` 保留 MCP server 入口和启动这些 server 所需的 API 凭据。
- `.env` 保存工作流通知路由值，也就是不适合维护在生成 state 里的发件人、收件人和 allowlist。

先在 `config.toml` 中填写 MCP 凭据占位符：

```toml
[mcp_servers.telegram_notifier.env]
TELEGRAM_BOT_TOKEN = "FILL_ME_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "FILL_ME_TELEGRAM_CHAT_ID"

[mcp_servers.resend.env]
RESEND_API_KEY = "FILL_ME_RESEND_API_KEY"
```

然后复制工作流通知配置示例：

```bash
cp .env.example .env
```

填写 `.env`：

```env
TELEGRAM_USER_IDS=FILL_ME_TELEGRAM_USER_ID

SENDER_EMAIL_ADDRESS=Codex Orchestrator <alerts@your-verified-domain.com>
RESEND_TO=you@example.com
RESEND_CC=
RESEND_BCC=
REPLY_TO_EMAIL_ADDRESSES=you@example.com
```

含义：

```text
TELEGRAM_USER_IDS         允许审批、拒绝、停止或重定向 run 的 Telegram 用户 ID，多个 ID 用逗号分隔。
SENDER_EMAIL_ADDRESS      已验证的 Resend 发件地址。
RESEND_TO                 接收 incident report 和长通知邮件的收件人，多个邮箱用逗号分隔。
RESEND_CC                 可选 CC 收件人，多个邮箱用逗号分隔。
RESEND_BCC                可选 BCC 收件人，多个邮箱用逗号分隔。
REPLY_TO_EMAIL_ADDRESSES  可选 reply-to 地址。默认情况下，邮件回复不是可执行审批。
```

`config.toml` 通过 `npx` 直接启动 Resend 和 Telegram，不再通过 Python wrapper 启动 MCP server。

`init_implement_doc_run.py` 创建新的 `.codex-orchestrator/implement-doc/state/*.json` 时，会读取 `.env`，并把这些工作流通知值复制进生成的 state。

如果 run 已经存在，它会继续使用已经生成的 state。若想让旧 run 使用新的通知配置，请新建 run，或者手动更新那个旧 state 文件。

## 获取 Telegram Token 和 ID

这个工作流里，Telegram 不是一个通用 API key，而是需要三个值：

```text
TELEGRAM_BOT_TOKEN  = bot 的 token，用于发送和读取消息；写入 config.toml
TELEGRAM_CHAT_ID    = 通知发送到哪个私聊、群组或频道；写入 config.toml
TELEGRAM_USER_IDS   = 允许审批、拒绝、停止或重定向 run 的用户 ID；写入 .env
```

Telegram 官方文档说明，bot token 由 `@BotFather` 生成；Bot API 使用 `getUpdates` 接收 incoming updates。

### 创建 Bot Token

1. 打开 Telegram。
2. 找到并打开 `@BotFather`。
3. 发送：

```text
/newbot
```

4. 按提示设置 bot 的显示名称和用户名。
5. 复制 BotFather 返回的 bot token，格式类似：

```text
123456789:AAExampleToken...
```

6. 写入 `config.toml`：

```toml
TELEGRAM_BOT_TOKEN = "123456789:AAExampleToken..."
```

### 获取 Chat ID

1. 和你的 bot 开始私聊，或者把 bot 加入你想接收通知的群组或频道。
2. 给 bot 或目标 chat 发送任意消息。
3. 调用 `getUpdates`：

```bash
curl "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates"
```

4. 找到 `chat.id` 字段：

```json
"chat": {
  "id": 123456789
}
```

把这个值写入 `config.toml`：

```toml
TELEGRAM_CHAT_ID = "123456789"
```

群组和超级群组的 chat ID 通常是负数，例如：

```text
-1001234567890
```

按 Telegram 返回的值原样填写。

### 获取你的 Telegram User ID，用于 allowlist

工作流还需要知道谁可以审批或重定向 run。这个值不一定等于 chat ID。

在同一个 `getUpdates` 返回里，找到你自己消息对应的 `from.id` 字段：

```json
"from": {
  "id": 123456789
}
```

把这个值写入 `.env`：

```env
TELEGRAM_USER_IDS=123456789
```

如果有多个允许审批的用户，用逗号分隔：

```env
TELEGRAM_USER_IDS=123456789,987654321
```

### 常见 Telegram 问题

- 如果 `getUpdates` 返回空数组，先给 bot 发一条新消息，再试一次。
- 如果 bot 在群组里，privacy mode 可能影响它能看到的消息。初次配置建议先用私聊测试。
- 如果使用群组或超级群组，`TELEGRAM_CHAT_ID` 要填 `chat.id`，不要填个人 `from.id`。
- `TELEGRAM_USER_IDS` 要填你的个人 `from.id`。

## 获取 Resend API Key 和发件配置

Resend 不只是填一个 API key。这个工作流需要：

```text
RESEND_API_KEY          = Resend API key，供 MCP server 使用；写入 config.toml
SENDER_EMAIL_ADDRESS    = 已验证域名下的发件地址；写入 .env
recipient email address = Codex incident report 发送到哪里；写入 .env
```

通常还需要先验证一个发信域名，Resend 才能稳定发送正式邮件。

### 验证发信域名

1. 注册或登录 Resend。
2. 打开 Resend dashboard。
3. 进入 Domains。
4. 添加域名。
5. 推荐使用子域名，例如：

```text
alerts.example.com
```

6. Resend 会显示需要添加到 DNS 服务商的记录。
7. 按 Resend 显示的内容逐条添加 DNS 记录。Resend 文档中说明 SPF 和 DKIM 是域名验证所需记录。
8. 等到 Resend dashboard 中域名状态变为 verified。

### 创建 Resend API Key

1. 打开 Resend dashboard。
2. 进入 API Keys。
3. 创建一个新的 API key。
4. 推荐选择 `Sending access`，不要默认选择 `Full access`。
5. 如果 Resend 支持按域名限制 key，就限制到你的通知域名。
6. 复制 key 并安全保存。Resend API key 是 secret。
7. 写入 `config.toml`：

```toml
RESEND_API_KEY = "re_..."
```

### 配置发件地址

域名验证通过后，Resend 允许从该域名下的地址发信。这个地址不一定要是真实 inbox，但建议使用可回复地址。

把发件人和可选 reply-to 地址写入 `.env`：

```env
SENDER_EMAIL_ADDRESS=Codex Orchestrator <alerts@alerts.example.com>
REPLY_TO_EMAIL_ADDRESSES=you@example.com
```

`REPLY_TO_EMAIL_ADDRESSES` 是可选项。默认情况下，工作流仍然把邮件视为通知通道，不把邮件回复作为可执行审批。

### 配置收件人邮箱

MCP server 只有在工作流提供收件人之后才能发邮件。把收件人写入 `.env`：

```env
RESEND_TO=you@example.com
RESEND_CC=
RESEND_BCC=
```

如果有多个收件人，用逗号分隔：

```env
RESEND_TO=owner@example.com,backup@example.com
```

新创建的 run state 会自动继承这些值。如果 run 已经存在，它会继续使用已经生成的 state；请新建 run，或者手动更新那个旧 state。

### Resend 最小检查清单

测试真实 Resend 邮件前，确认：

- `RESEND_API_KEY` 以 `re_` 开头；
- 发送域名在 Resend 中已经 verified；
- `SENDER_EMAIL_ADDRESS` 使用这个已验证域名；
- `RESEND_TO` 至少包含一个收件人邮箱；
- 收件人邮箱能接收外部邮件。

## 本地 smoke test

在这个 `.codex` 目录下运行：

```bash
python3 -m py_compile skills/implement-doc/scripts/*.py
```

```bash
python3 - <<'PY'
import json, tomllib
from pathlib import Path
for path in sorted(Path("skills/implement-doc/assets").glob("*.json")):
    json.loads(path.read_text(encoding="utf-8"))
with Path("config.toml").open("rb") as f:
    tomllib.load(f)
print("json/toml ok")
PY
```

```bash
CODEX_HOME=/home/kunorikiku/source/codex-workflow-deploy codex mcp list
```

测试 helper scripts：

```bash
skills/implement-doc/scripts/make_artifact_name.py --kind report --task-id M1-T1 --title "GPU contact filter" --ext md
```

```bash
skills/implement-doc/scripts/classify_incident.py --text "blocked by missing dependency and user decision required"
```

```bash
skills/implement-doc/scripts/parse_remote_reply.py --reply "C 8KQ2" --nonce 8KQ2 --run-id test-run --incident-id inc-1
```

```bash
skills/implement-doc/scripts/init_implement_doc_run.py --repo-root . --roadmap-doc roadmap.md --title "smoke test" --force-new
```

initializer 会创建 `.codex-orchestrator/implement-doc/...` 运行时目录。

## 真实通道测试

在 `config.toml` 填入真实凭据、在 `.env` 填入通知路由后，用这个目录作为 `CODEX_HOME` 启动 Codex，然后测试 Telegram：

```text
Use telegram_notifier.send_message to send me: "Codex Telegram MCP test OK"
```

然后测试 Resend：

```text
Use resend to send a test email to <your-email> with subject "Codex Resend MCP test" and body "Resend notification path is working."
```

两个通道都成功后，再开始真实实现 run。

## 运行流程

1. 打开包含 roadmap、SPEC 或实现文档的项目 repo。
2. 在项目根目录启动 Codex，并指定本目录为 `.codex` home：

```bash
CODEX_HOME=/home/kunorikiku/source/codex-workflow-deploy codex
```

3. 使用 slash prompt：

```text
/prompts:implement-doc DOC=docs/roadmap.md TITLE="my project implementation"
```

或者直接调用 skill：

```text
$implement-doc

Implement as per the doc under docs/roadmap.md says.

Title: my project implementation

Use the current repository root.
```

4. controller 读取 roadmap，并在项目中创建或复用 state：

```text
.codex-orchestrator/implement-doc/state/
```

5. controller 给持久 worker 分配一个 bounded task。
6. worker 写代码，并把报告写到：

```text
.codex-orchestrator/implement-doc/reports/
```

7. controller 执行轻量验证：

```bash
git status --short
git diff --name-status
git diff --stat
git diff --check
```

8. 如果结果安全，controller 继续下一个 bounded task。
9. 如果发现严重问题，controller 写 incident report 和 notification artifacts。
10. 对 SEV0-SEV2，Resend 发送长报告邮件，Telegram 发送短决策提示。
11. 你在 Telegram 中按规定格式回复。

## Telegram 远程决策格式

每个可执行回复都必须带上通知里的 nonce：

```text
A <nonce>
B <nonce>
C <nonce>
D <nonce>
E <nonce>
F <nonce>
CUSTOM <nonce> <freeform instruction>
```

含义：

```text
A      继续当前路线，之后再更新 roadmap。
B      回滚 worker 本次任务的修改。
C      保留部分修改，但重定向实现方向。
D      暂停，等待用户提供新的 roadmap 章节。
E      停止本次实现 run。
F      先运行只读 verifier audit。
CUSTOM 按用户自定义 controller 指令执行。
```

示例：

```text
C 8KQ2
```

自定义示例：

```text
CUSTOM 8KQ2 keep the GPU filtering changes, but revert public solver API changes
```

controller 必须验证：

- Telegram sender user ID 在 allowlist 中；
- nonce 匹配当前 pending incident；
- 回复格式受支持；
- decision 已写入 `.codex-orchestrator/implement-doc/remote-decisions/`。

## 安全规则

- 如果 Codex 支持 profile 级 MCP 隔离，不要把 `codex_worker` 暴露给 worker profile。
- 除非环境是一次性容器且你明确接受风险，否则 worker session 不要用 `danger-full-access`。
- 默认不要把 Resend inbound email 当作可执行审批。
- 默认不要使用 Telegram inline keyboard。
- 默认不要使用 Signal。
- SEV0-SEV2 未得到有效 Telegram 决策、直接用户指令或 roadmap 更新前，不要继续。
- 不要把 API key 提交到 git 或写进日志。
- `config.toml` 默认只有 API key 占位符。如果你填入真实凭据后要发布 fork，请先移除真实值。

## 故障排查

如果 `codex mcp list` 看不到 server，检查：

```bash
echo "$CODEX_HOME"
```

确认 `config.toml` 在该目录下。

如果 Telegram server 能启动但收不到消息：

- 检查 `config.toml` 里的 `TELEGRAM_BOT_TOKEN`；
- 检查 `config.toml` 里的 `TELEGRAM_CHAT_ID`；
- 先给 bot 发一条消息；
- 如果是群组，确认 bot 已加入群组；
- 用 `getUpdates` 确认 Telegram 返回的 chat ID。

如果 Resend 能启动但发信失败：

- 检查 `config.toml` 里的 `RESEND_API_KEY`；
- 检查 Resend 里的发送域名是否 verified；
- 确认 SPF 和 DKIM 已验证；
- 确认 `.env` 里的 `SENDER_EMAIL_ADDRESS` 使用已验证域名；
- 确认 `.env` 里的 `RESEND_TO` 不是空值。

如果 `triage_diff.sh` 提示不是 Git worktree，请在项目 repo 中运行，而不是在这个 `.codex` home 里运行。

## 官方参考

- Telegram bots 与 BotFather: https://core.telegram.org/api/bots
- Telegram Bot API `getUpdates`: https://core.telegram.org/bots/api#getupdates
- Resend API keys: https://resend.com/docs/dashboard/api-keys/introduction
- Resend 域名验证: https://resend.com/docs/dashboard/domains/introduction
- Resend 发件地址说明: https://resend.com/docs/knowledge-base/how-do-I-create-an-email-address-or-sender-in-resend
