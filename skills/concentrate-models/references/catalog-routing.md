# Model catalog and routing

Official sources: [List Models](https://concentrate.ai/docs/api-reference/endpoint/list-models), [Get Model](https://concentrate.ai/docs/api-reference/endpoint/get-model), [List Providers](https://concentrate.ai/docs/api-reference/endpoint/list-providers), [Supported Models](https://concentrate.ai/docs/api-reference/endpoint/supported-models), and [Auto Routing](https://concentrate.ai/docs/api-reference/endpoint/auto-routing).

## Public catalog endpoints

These endpoints do not require authentication:

```text
GET /v1/models
GET /v1/models/{model}
GET /v1/models/{model}/providers/{provider}
GET /v1/models/providers
GET /v1/models/providers/{provider}/models
GET /v1/models/authors/{author}
```

`GET /v1/models` returns the combined OpenAI-compatible shape with `data[]`, basic limits, and normalized capability summaries. `GET /v1/models/{model}` returns the native detail shape with per-provider pricing, `supports`, `image_processing`, `pdf_processing`, and `zdr`. Use model detail when provider-specific behavior matters.

The list endpoint accepts documented dot-notation filters. Equality filters and numeric suffixes (`.gte`, `.lte`, `.gt`, `.lt`) are ANDed. Examples:

```text
/v1/models?author.slug=anthropic
/v1/models?supports.streaming=true&context_window.gte=128000
/v1/models?supports.tools.function_calling=true
```

## Model identifiers

- Bare model slug, such as `gpt-4o`: Concentrate chooses a provider.
- Provider-prefixed slug, such as `openai/gpt-4o`: starts with that provider but may fall back to another provider for the same model if it fails.
- `auto`: Concentrate selects a compatible model from a curated pool. Model-based optimization is currently simplified; `routing.model.sort` is documented but currently not applied to model selection.

The prefix is the serving provider, not necessarily the model author.

## Routing

```json
{
  "model": "gpt-4o",
  "input": "Summarize this text.",
  "routing": {
    "provider": {
      "sort": "cost",
      "interval": "15m",
      "fallbacks": ["openai", "azure"]
    },
    "model": {
      "fallbacks": ["gemini-2.5-flash", "auto"]
    }
  }
}
```

`routing.provider.fallbacks` is a provider whitelist despite its name. Provider sort supports static `cost` and `performance`, plus documented live metrics such as latency percentiles, uptime, throughput, request counts, and token counts. Live metric windows have a 15-minute minimum.

Routing matches request features, prefers cache affinity, excludes unhealthy feature routes, retries eligible providers, and may degrade optional features if no route supports everything. Streaming failover stops once the stream begins. With a ZDR key, non-ZDR providers are never considered and lack of an eligible path produces 422.

## Presenting comparisons

Use live data and state when it was queried. Compare per-provider context/output limits, input/output price units, relevant `supports` flags, ZDR status, and deprecation fields. Do not reduce model choice to one universal ranking; match it to the user's capability, budget, latency, provider, and data-policy constraints.
