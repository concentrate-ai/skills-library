# Concentrate AI Skills & Plugin Library

A comprehensive collection of [Agent Skills](https://agentskills.io) and plugins for building with [Concentrate AI](https://concentrate.ai) — the unified gateway for **170+ AI models**, cost/latency auto-routing, and Zero Data Retention (ZDR) privacy.

These skills empower AI coding assistants (including **Claude Code**, **Cursor**, **OpenCode**, **Gemini CLI**, **Windsurf**, and **OpenAI Codex**) to generate accurate, type-safe, zero-hallucination code for Concentrate AI APIs.

---

## 📦 Installation & Setup

### 1. Claude Code
Install as a native Claude Code plugin:
```bash
/plugin marketplace add AjayK47/skills-library
/plugin install concentrate@concentrate
```

### 2. GitHub CLI (`gh skill`)
Works with Claude Code, Cursor, OpenCode, Codex, Gemini CLI, and Windsurf (requires GitHub CLI v2.90.0+):

```bash
# Install all Concentrate skills
gh skill install AjayK47/skills-library

# Or install a specific skill (e.g., ZDR privacy)
gh skill install AjayK47/skills-library concentrate-zdr

# Install at user scope (across all projects)
gh skill install AjayK47/skills-library --scope user
```

### 3. Cursor
1. Go to **Settings** → **Rules** → **Add Rule** → **Remote Rule (GitHub)**.
2. Enter repository: `AjayK47/skills-library`.

### 4. OpenCode
```bash
git clone https://github.com/AjayK47/skills-library.git /tmp/concentrate-skills
cp -r /tmp/concentrate-skills/skills/* ~/.config/opencode/skills/
rm -rf /tmp/concentrate-skills
```

---

## 🛠️ Included Skills

| Skill | Description | Triggers / Use Cases |
| :--- | :--- | :--- |
| [`concentrate-responses`](./skills/concentrate-responses/SKILL.md) | Standard `POST /v1/responses` usage, structured outputs (`json_schema`), multi-turn loops, SSE streaming, and tool calling. | Generating text/code, tool calling, JSON schema outputs, streaming responses. |
| [`concentrate-models`](./skills/concentrate-models/SKILL.md) | Model discovery, provider prefixes (`bedrock/...`, `openai/...`), and dynamic auto-routing (`model: "auto"` with sort by cost/latency). | Model selection, provider routing, benchmarking, pricing optimization. |
| [`concentrate-zdr`](./skills/concentrate-zdr/SKILL.md) | Enterprise privacy routing across 104+ Zero Data Retention certified models/providers (`bedrock`, `azure`, `vertex`, etc.). | Enterprise compliance, HIPAA, fintech, legal, zero-data retention enforcement. |
| [`concentrate-multimodal`](./skills/concentrate-multimodal/SKILL.md) | Sending base64 and URL images to 100+ vision-capable models with detail level controls. | Image analysis, OCR, visual document parsing, UI comparison. |
| [`concentrate-integrations`](./skills/concentrate-integrations/SKILL.md) | Setting up Claude Code, Cursor, Python/TypeScript OpenAI SDKs, LangChain, and LlamaIndex with Concentrate AI. | IDE configuration, OpenAI client base URL overrides, pay-as-you-go setup. |

---

## 🔑 Environment Setup

All Concentrate AI requests require an API key:
```bash
export CONCENTRATE_API_KEY="your_api_key_here"
```
Get an API key from the [Concentrate AI Dashboard](https://concentrate.ai).

---

## 📚 Official Resources

* [Concentrate AI Website](https://concentrate.ai)
* [Documentation & API Reference](https://concentrate.ai/docs)
* [Models Catalog & Pricing](https://concentrate.ai/models)
* [Documentation Index (llms.txt)](https://concentrate.ai/docs/llms.txt)

---

## 📄 License
MIT License. See [LICENSE](./LICENSE) for details.
