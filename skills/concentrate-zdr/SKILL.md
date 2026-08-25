---
name: concentrate-zdr
description: Configure and enforce Zero Data Retention (ZDR) and enterprise privacy compliance on Concentrate AI. Use when building applications for healthcare (HIPAA), fintech, legal, or GDPR compliance, configuring privacy-first routing, targeting ZDR-certified providers (`bedrock/...`, `azure/...`, `vertex/...`), or understanding ZDR key enforcement.
---

# Concentrate AI Zero Data Retention (ZDR) & Privacy

Concentrate AI provides **Zero Data Retention (ZDR)** guarantees across **104+ certified models and providers**. When ZDR is enforced, prompts and completions are strictly processed in-memory and never stored, logged, or used for model training by upstream providers.

---

## 1. How ZDR Works

* **Certified Endpoints Only:** Requests are strictly routed to providers with binding, audited zero-data-retention agreements.
* **Strict Fail-Safe Enforcement:** Concentrate will **never** silently fall back to a non-ZDR provider. If no ZDR-certified provider is available for the requested model, the API immediately returns an explicit `422` error.
* **Key-Level & Org-Level Enforcement:** ZDR can be locked at the API key level or organization-wide in the Concentrate Dashboard.

---

## 2. Certified ZDR Provider Slugs

When targeting specific backends or inspecting model capabilities, the following provider slugs offer ZDR certification:

| Provider Slug | Cloud / Backend | Typical Certified Models |
| :--- | :--- | :--- |
| `bedrock` | AWS Bedrock | Claude Sonnet/Opus, Llama 3.3/4, Mistral Large |
| `vertex` | Google Cloud Vertex AI | Gemini 3.6/3.1/2.5 Pro & Flash, Gemma |
| `azure` / `azure-fw` | Microsoft Azure AI | GPT-5.6, GPT-4o, o3-mini |
| `openai` | Direct OpenAI (ZDR Tier) | GPT-5.6 Sol/Terra, GPT-4o, o1 |
| `anthropic` | Direct Anthropic (ZDR Tier) | Claude Opus 5, Claude Sonnet 5 |
| `deepinfra` | DeepInfra Enterprise | Llama 3.3, Qwen 3.5, DeepSeek R1 |
| `fireworks` | Fireworks AI Enterprise | Qwen 3 Coder, Llama 3.3 |
| `novita` | Novita AI Enterprise | DeepSeek V3/R1 |

---

## 3. Explicit ZDR Routing Examples

### A. Targeting a ZDR Provider Prefix
To explicitly guarantee that a request routes through a ZDR-certified cloud environment (like AWS Bedrock or Google Vertex):

```json
{
  "model": "bedrock/claude-opus-4-8",
  "input": "Review this patient summary for clinical code classification."
}
```

```json
{
  "model": "vertex/gemini-2.5-pro",
  "input": "Audit this confidential financial statement."
}
```

### B. Using an API Key with ZDR Enabled
When an API key has ZDR enabled in the Concentrate Dashboard:
1. You can use standard model names like `"model": "gpt-5.6-sol"`.
2. Concentrate's routing engine automatically filters out all non-ZDR providers and only routes to certified instances (e.g. Azure ZDR or OpenAI Enterprise ZDR).

---

## 4. Handling ZDR Validation Errors (`422`)

If a model does not have any ZDR-certified provider available, the API returns:

```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Zero Data Retention (ZDR) is enabled, but there are no available providers or models that support it for this request."
  }
}
```

### Error Handling Pattern (TypeScript):
```typescript
try {
  const response = await fetch("https://api.concentrate.ai/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.CONCENTRATE_ZDR_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "bedrock/llama-3.3-70b-instruct",
      input: "Sensitive compliance query..."
    })
  });

  if (response.status === 422) {
    console.error("ZDR Error: No certified ZDR provider available for this model configuration.");
  }
} catch (err) {
  console.error(err);
}
```

---

## 5. PII Redaction & Guardrails (`redact-v1`)

For extra privacy before sending data to models, you can invoke Concentrate's dedicated redaction model:

```bash
curl https://api.concentrate.ai/v1/responses \
  -H "Authorization: Bearer YOUR_CONCENTRATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "redact-v1",
    "input": "Patient John Doe (SSN: 000-12-3456) visited Dr. Smith at 123 Main St."
  }'
```
*Key-level guardrails can also be enabled in the dashboard to automatically redact sensitive PII (names, SSNs, credit cards, emails) before prompts reach upstream LLMs.*
