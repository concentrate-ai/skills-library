---
name: concentrate-models
description: Model discovery, provider selection, and cost/latency auto-routing for Concentrate AI. Use when selecting AI models, configuring automatic provider routing (`model: "auto"` or `routing.provider.sort`), setting provider prefixes (`anthropic/...`, `bedrock/...`, `openai/...`), or querying available models from 170+ LLMs.
---

# Concentrate AI Models & Intelligent Routing

Concentrate AI provides access to **170+ models across 21 authors and providers**. You can target models directly, pin specific upstream providers, or configure intelligent dynamic routing based on cost, latency, uptime, or throughput.

---

## 1. Model Selection Formats

You can specify models in the `model` field using 3 strategies:

### A. Automatic Provider Routing (Model Slug Only)
Specifies the model, and Concentrate automatically chooses the fastest and most cost-effective upstream provider:
```json
{
  "model": "gpt-5.6-sol",
  "input": "Explain the theory of relativity."
}
```

### B. Pinned Provider (`provider/model`)
Pins execution to a specific provider backend (e.g. AWS Bedrock, Google Vertex, Azure, OpenAI, Anthropic):
```json
{
  "model": "anthropic/claude-opus-4-8",
  "input": "Analyze this code."
}
```
*Note: If the pinned provider experiences an outage, Concentrate's multi-provider fallback can gracefully route to alternate providers for the same model.*

### C. Auto Model Selection (`model: "auto"`)
Allows Concentrate to select a high-capability model from a curated pool automatically:
```json
{
  "model": "auto",
  "input": "Summarize this article.",
  "routing": {
    "provider": { "sort": "cost" }
  }
}
```

---

## 2. Dynamic Routing Configuration

Customize provider sorting and filtering using the `routing` parameter:

```json
{
  "model": "llama-3.3-70b-instruct",
  "input": "Generate a sales email.",
  "routing": {
    "provider": {
      "sort": "cost",
      "interval": "15m",
      "allow": ["bedrock", "deepinfra", "fireworks"],
      "deny": ["novita"]
    }
  }
}
```

### Supported Sort Metrics

#### Static Metrics
* `"cost"`: Routes to the cheapest provider first.
* `"performance"`: Routes to the highest-quality tier first.

#### Live Observability Metrics (Computed over real-time windows)
* `"avg_latency"`: Lowest average response time.
* `"p50_latency"` / `"p90_latency"` / `"p99_latency"`: Target specific latency percentiles.
* `"avg_e2e_latency"`: Total round-trip latency including network overhead.
* `"uptime"`: Highest provider availability percentage.
* `"throughput"`: Maximum sustained tokens/second.

#### Calculation Interval (`interval`)
* `"15m"` or `"15 minutes"` (default)
* `"1h"` or `"1 hour"`

---

## 3. Popular Models Quick Reference

| Author | Recommended Model Slugs | Ideal For |
| :--- | :--- | :--- |
| **OpenAI** | `gpt-5.6-sol`, `gpt-5.5`, `gpt-5.4-pro`, `gpt-5.3-codex`, `gpt-4o`, `o3-mini`, `o1` | Complex reasoning, code generation, general problem solving |
| **Anthropic** | `claude-fable-5`, `claude-opus-5`, `claude-opus-4-8`, `claude-sonnet-5`, `claude-haiku-4-5` | Deep analysis, long-context comprehension, nuanced coding |
| **Google** | `gemini-3.6-flash`, `gemini-3.1-pro-preview`, `gemini-2.5-pro`, `gemma-4-31b` | Massive context windows, multimodal reasoning, low-latency search |
| **xAI** | `grok-4.5`, `grok-4.3`, `grok-4.20-0309-reasoning`, `grok-build-0.1` | High-speed reasoning and code tasks |
| **Mistral** | `mistral-large-3`, `codestral`, `devstral-2`, `ministral-3-14b` | Code generation, European data residency compliance |
| **Alibaba** | `qwen3.8-max`, `qwen3.7-plus`, `qwen3-coder-plus`, `qwen3-vl-plus` | Multilingual tasks, specialized coding, vision analysis |
| **DeepSeek** | `deepseek-v4-pro`, `deepseek-v4-flash`, `deepseek-r1`, `deepseek-v3-2` | Cost-effective advanced reasoning and mathematical problem-solving |
| **Meta** | `llama-4-maverick`, `llama-4-scout`, `llama-3.3-70b-instruct` | Open-weights flexibility, cost-effective deployments |

---

## 4. Querying the Live Catalog API

### List All Models
```bash
curl https://api.concentrate.ai/v1/models \
  -H "Authorization: Bearer YOUR_CONCENTRATE_API_KEY"
```

### Inspect a Specific Model
```bash
curl https://api.concentrate.ai/v1/models/gpt-5.6-sol \
  -H "Authorization: Bearer YOUR_CONCENTRATE_API_KEY"
```

### List Providers
```bash
curl https://api.concentrate.ai/v1/providers \
  -H "Authorization: Bearer YOUR_CONCENTRATE_API_KEY"
```
