# Concentrate AI Skills

A collection of [Agent Skills](https://agentskills.io) for building with [Concentrate AI](https://concentrate.ai) — a unified API for [170+ AI models](https://concentrate.ai/models), automatic cost/latency routing, and Zero Data Retention (ZDR) privacy.

These skills work with any agent that supports the Agent Skills standard, including Claude Code, Cursor, OpenCode, Codex, and Gemini CLI. For agents that support plugins, installing via the native plugin system is recommended as skills will auto-update.

## Install

### Claude Code

```text
/plugin marketplace add AjayK47/skills-library
/plugin install concentrate@concentrate
```

### GitHub CLI (`gh skill`)

```bash
gh skill install AjayK47/skills-library
```

To install a specific skill:

```bash
gh skill install AjayK47/skills-library concentrate-models
```

### Cursor

Add via **Settings → Rules → Add Rule → Remote Rule (GitHub)** with `AjayK47/skills-library`.

### OpenCode

```bash
git clone https://github.com/AjayK47/skills-library.git /tmp/concentrate-skills
cp -r /tmp/concentrate-skills/skills/* ~/.config/opencode/skills/
rm -rf /tmp/concentrate-skills
```

## Skills

Skills are contextual and auto-loaded based on your conversation. When a request matches a skill's triggers, your AI coding agent loads and applies the relevant skill to provide accurate, up-to-date guidance.

| Skill | Description |
|---|---|
| [`concentrate-responses`](skills/concentrate-responses/SKILL.md) | Standard Responses API (`/v1/responses`), stateful turns, function tools, structured JSON output, web search, SSE streaming, and caching |
| [`concentrate-models`](skills/concentrate-models/SKILL.md) | Model catalog discovery, provider prefixes (`bedrock/...`, `anthropic/...`), dynamic cost/latency routing, and capabilities |
| [`concentrate-multimodal`](skills/concentrate-multimodal/SKILL.md) | Vision input processing, base64 and URL image inputs, format support, and resolution detail controls |
| [`concentrate-data-controls`](skills/concentrate-data-controls/SKILL.md) | Zero Data Retention (ZDR), request logging, PII redaction guardrails (`redact-v1`), and Bring Your Own Key (BYOK) |
| [`concentrate-integrations`](skills/concentrate-integrations/SKILL.md) | Client setups (Claude Code, Cursor, OpenAI/Anthropic SDKs) and migrations from other gateways (OpenRouter, LiteLLM, Vercel, etc.) |
| [`concentrate-alerts`](skills/concentrate-alerts/SKILL.md) | Account alerts for spend anomalies, error spikes, key limits, dormant keys, and recurring usage reports |

## Environment

All authenticated inference requests require an API key from the [Concentrate dashboard](https://concentrate.ai):

```bash
export CONCENTRATE_API_KEY="your_api_key_here"
```

## Resources

- [Concentrate Website](https://concentrate.ai)
- [Concentrate Documentation](https://concentrate.ai/docs)
- [API Reference](https://concentrate.ai/docs/api-reference/introduction)
- [Models Catalog](https://concentrate.ai/models)

## License

MIT. See [LICENSE](LICENSE).
