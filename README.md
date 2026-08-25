# Concentrate AI Skills

Agent Skills for building with [Concentrate AI](https://concentrate.ai), grounded in the documentation published by the Concentrate AI team.

The library follows the useful parts of the [OpenRouter skills repository](https://github.com/OpenRouterTeam/skills): narrowly triggered skills, progressive references, live discovery scripts where data changes frequently, and native plugin metadata. It intentionally does not include image generation, speech-to-text, text-to-speech, video, OAuth, analytics-query, or a dedicated SDK skill because those surfaces are not documented by Concentrate today.

## Install

These folders use the [Agent Skills](https://agentskills.io) format and work with agents that support it.

### Claude Code plugin

```text
/plugin marketplace add AjayK47/skills-library
/plugin install concentrate@concentrate
```

### GitHub CLI

```bash
gh skill install AjayK47/skills-library
```

Install one skill by adding its folder name, for example:

```bash
gh skill install AjayK47/skills-library concentrate-models
```

### Cursor

In **Settings → Rules → Add Rule → Remote Rule (GitHub)**, enter `AjayK47/skills-library`.

### OpenCode

```bash
git clone https://github.com/AjayK47/skills-library.git /tmp/concentrate-skills
cp -r /tmp/concentrate-skills/skills/* ~/.config/opencode/skills/
rm -rf /tmp/concentrate-skills
```

## Skills

| Skill | Use it for |
|---|---|
| [`concentrate-responses`](skills/concentrate-responses/SKILL.md) | Responses API requests, stateful turns, tools, structured output, web search, streaming, caching, and errors |
| [`concentrate-models`](skills/concentrate-models/SKILL.md) | Live model/provider discovery, capability checks, comparisons, routing, and fallbacks |
| [`concentrate-multimodal`](skills/concentrate-multimodal/SKILL.md) | Image inputs, supported formats, model/provider capability checks, and limits |
| [`concentrate-data-controls`](skills/concentrate-data-controls/SKILL.md) | ZDR, request logging, guardrails, `redact-v1`, and BYOK |
| [`concentrate-integrations`](skills/concentrate-integrations/SKILL.md) | Supported clients, compatibility endpoints, and migrations from other gateways |
| [`concentrate-alerts`](skills/concentrate-alerts/SKILL.md) | Choosing and configuring documented spend, balance, key, error, and reporting alerts |

## Environment

Authenticated inference requests use an API key from the [Concentrate dashboard](https://concentrate.ai):

```bash
export CONCENTRATE_API_KEY="your_api_key_here"
```

Never commit API keys. The public model-catalog endpoints and the model discovery script do not require a key.

## Source policy

- Prefer the live [`GET /v1/models`](https://api.concentrate.ai/v1/models) catalog for model names and capabilities; these change faster than skills should.
- Prefer the official [documentation index](https://concentrate.ai/docs/llms.txt) and [OpenAPI specification](https://concentrate.ai/docs/api-reference/openapi.json) for behavior and schemas.
- Treat Chat Completions and Messages compatibility as beta. Prefer the Responses API for production, as the official docs recommend.
- Do not claim Concentrate supports a modality, endpoint, integration, or SDK unless it is present in the official docs.

## Official resources

- [Documentation](https://concentrate.ai/docs)
- [Documentation index](https://concentrate.ai/docs/llms.txt)
- [API introduction](https://concentrate.ai/docs/api-reference/introduction)
- [OpenAPI specification](https://concentrate.ai/docs/api-reference/openapi.json)
- [Models catalog](https://concentrate.ai/models)

## License

MIT. See [LICENSE](LICENSE).
