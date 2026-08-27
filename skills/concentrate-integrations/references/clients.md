# Client integrations and compatibility APIs

Official sources: [Integrations overview](https://concentrate.ai/docs/integrations/overview), [Claude Code](https://concentrate.ai/docs/integrations/claude-code), [Claude Desktop](https://concentrate.ai/docs/integrations/claude-desktop), [Codex](https://concentrate.ai/docs/integrations/codex), [Cursor](https://concentrate.ai/docs/integrations/cursor), [Chat Completions](https://concentrate.ai/docs/api-reference/endpoint/chat-completions), and [Messages](https://concentrate.ai/docs/api-reference/endpoint/create-message).

## Base URLs

| Client family | Base URL | Why |
|---|---|---|
| OpenAI-compatible clients and SDKs | `https://api.concentrate.ai/v1` | Client appends endpoint paths such as `/chat/completions` |
| Anthropic-native clients | `https://api.concentrate.ai` | These clients append `/v1`; including it produces `/v1/v1/...` |

Concentrate accepts `Authorization: Bearer ...` and `x-api-key: ...`; bearer auth takes precedence if both are sent.

## Claude Code

The official manual setup uses shell-profile variables:

```bash
export CONCENTRATE_API_KEY="your_api_key_here"
export ANTHROPIC_BASE_URL="https://api.concentrate.ai"
export ANTHROPIC_AUTH_TOKEN="$CONCENTRATE_API_KEY"
export ANTHROPIC_API_KEY=""
```

Claude Code does not read a project `.env` for this setup. A user previously logged into Anthropic may need `/logout`. After reloading the shell, verify with `/status`; it should show the Concentrate endpoint. Use `/model <model>` to switch, but query the live catalog's Claude Code compatibility data instead of assuming every model works equally well.

## Claude Desktop

Use the Cowork third-party platform gateway with base URL `https://api.concentrate.ai`, bearer auth, and exact `provider/model` slugs. The official guide contains a narrow allowlist for its 1M-context UI toggle; do not enable that toggle for other models without updated documentation.

## Cursor and generic OpenAI clients

Chat Completions compatibility is beta. Configure the OpenAI-compatible base URL and Concentrate key, then use a live model slug. Prefer the native Responses API for production application code.

## Codex

The official Codex page currently says the integration is unsupported and nonfunctional. Do not offer a setup recipe until that page changes.

## Compatibility boundary

`POST /v1/chat/completions` and `POST /v1/messages` are beta compatibility endpoints. Keep their schemas native to the client; do not paste Responses tool objects into Chat Completions or Messages payloads without converting the shape.
