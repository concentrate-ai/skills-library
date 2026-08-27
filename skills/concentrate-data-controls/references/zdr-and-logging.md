# ZDR and request logging

Official source: [Zero Data Retention & Logging](https://concentrate.ai/docs/api-reference/endpoint/zero-data-retention).

## Separate controls

- ZDR restricts upstream routing to certified model/provider pairs so prompts and completions are not stored by the upstream provider.
- Request logging controls whether Concentrate stores encrypted request and response content for history and audit.

Both are configured per key in the dashboard and may be enforced from organization, team, or user scope. Each field is resolved independently. Logging is disabled by default; ZDR is disabled by default.

When logging is disabled, Concentrate still records operational and billing metadata such as key reference, URL/status, elapsed time, resolved model/provider, token usage, and cost. It does not store prompt or completion content under that setting.

## Verify ZDR live

`GET /v1/models` does not contain per-provider ZDR evidence. Query:

```text
GET https://api.concentrate.ai/v1/models/{model}
```

For each provider, `zdr` is either `false` or an object with policy/certificate URLs. Only the object form qualifies. Model counts and certified provider lists change, so do not rely on copied tables.

With ZDR enabled on the calling key, routing excludes every non-ZDR provider. If no certified route supports the model and required features, Concentrate returns 422 and does not silently downgrade to non-ZDR.

You may combine ZDR with `routing.provider.fallbacks` to restrict the eligible certified provider subset further.
