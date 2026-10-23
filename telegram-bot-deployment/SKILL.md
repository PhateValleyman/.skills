---
name: telegram-bot-deployment
description: Deploy, host, secure and operate Telegram bots and userbots (systemd service, Docker/compose, webhook behind nginx or Caddy with TLS, Tailscale/NAS/Raspberry Pi hosting, secret handling, logging, health checks, rate-limit and error handling, Local Bot API Server). Use whenever the user asks how to run a Telegram bot 24/7, set up a webhook, make a bot restart on boot, containerize it, or troubleshoot a bot that stops responding.
---

# Telegram bot deployment & operations

## Pick the hosting model

| Situation | Recommendation |
|---|---|
| Home server / NAS / RPi, no public IP | **Long polling** (outbound only). No webhook, no port forwarding |
| VPS with domain | Webhook behind nginx/Caddy (TLS), or polling; both fine |
| Serverless (Cloud Run, Lambda, Workers) | Webhook; keep handler fast, ack quickly, queue slow work |
| Need >50 MB files | Local Bot API Server or MTProto client (`telegram-bot-api`, `telegram-client-api` skills) |

Old/limited devices (e.g. ARMv5 NAS): prefer a single static binary (Go, cross-compiled elsewhere) or a tiny stdlib Python script (`telegram-bot-api/scripts/tg_bot.py`) over heavy runtimes.

## Secrets

- Env file `/etc/tgbot/bot.env`, `chmod 600`, owned by the service user; or systemd `EnvironmentFile=` / Docker secrets.
- Never put tokens in git, Docker images, logs or screenshots. The token is in the URL path of every API call, so scrub proxy/access logs.
- Rotate with BotFather `/revoke`. Rotate StringSessions by terminating the session in Telegram > Devices.

## systemd (polling bot)

Template: `assets/tgbot.service`.
```bash
sudo useradd -r -s /usr/sbin/nologin tgbot
sudo mkdir -p /etc/tgbot /opt/tgbot/data && sudo chown tgbot /opt/tgbot/data
sudo install -m 600 -o tgbot bot.env /etc/tgbot/bot.env
sudo cp assets/tgbot.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now tgbot
journalctl -u tgbot -f
```

## Docker

Templates: `assets/Dockerfile`, `assets/docker-compose.yml` (bot + optional Local Bot API server). Use `restart: unless-stopped`, a volume for state/sessions, non-root user. Verify the Local Bot API image name upstream before using it.

## Webhook behind nginx

Template: `assets/nginx-webhook.conf`. Checklist:
1. Valid TLS cert for your domain (Let's Encrypt). Telegram accepts only ports 443, 80, 88, 8443.
2. Random URL path *and* `secret_token` in `setWebhook`; verify header `X-Telegram-Bot-Api-Secret-Token`.
3. Reply `200` fast; do slow work in a background task/queue. Telegram retries on non-2xx/timeouts and may deliver duplicates, so make handlers idempotent using `update_id`.
4. `getWebhookInfo` shows `last_error_message` and `pending_update_count`; check it first when the bot is silent.
5. `max_connections` (1-100) tunes concurrency; `drop_pending_updates=true` on `setWebhook`/`deleteWebhook` clears the backlog.

No public exposure wanted? Use polling, or tunnel only the webhook path (Tailscale Funnel / Cloudflare Tunnel).

## Reliability patterns

- Wrap handlers in try/except, log with update id, alert yourself on crash loops.
- 429: honor `retry_after`; queue outgoing messages and throttle (~1/s per chat, ~30/s global).
- 403 blocked: mark user inactive. 400 chat not found: drop.
- Persist state (SQLite/Postgres/Redis), not in-memory dicts.
- Health check: periodic `getMe` plus a heartbeat; alert if `pending_update_count` keeps growing.
- One poller per token. Duplicate instances give 409 Conflict. Stop the old instance before starting the new one.
- Handle SIGTERM gracefully so in-flight updates finish.

## Troubleshooting flow

1. `getMe` OK? (token valid)
2. `getWebhookInfo` (url empty when polling? error text?)
3. Logs for 409 / 429 / 403
4. Network egress to `api.telegram.org:443` (firewall, DNS, IPv6, proxy)
5. Clock skew (TLS)
6. Groups: privacy mode, bot is admin, correct `chat_id` sign

## Template adaptation and safe deployment
Read templates relative to this SKILL.md; copy them into the bot project, not the live system, before editing. Dockerfile expects the project's own requirements.txt and bot.py; these are not bundled bot implementations. Add a .dockerignore excluding .env, sessions, tokens, private keys, VCS metadata and private state before building, because COPY . . would otherwise bake them into an image. The optional local-api Compose service now requires its explicit profile; pin/verify its image and configure bot-to-service networking before use. Replace the example webhook path with a fresh value and verify the secret-token header in the handler, not merely in nginx. Run syntax/config checks and a smoke test before enabling services. Check whether tgbot already exists; do not blindly recreate accounts or replace a service. drop_pending_updates intentionally destroys queued updates: use only when explicitly requested. Inspect current Telegram documentation before relying on the historical size/rate-limit figures above.
