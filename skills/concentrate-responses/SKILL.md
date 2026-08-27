---
name: concentrate-responses
description: Build and troubleshoot Concentrate AI Responses API requests, including stateful turns, function tools, structured JSON, web search, streaming, prompt caching, usage, cost, and errors. Use for native Concentrate inference code; use the integrations skill when a third-party client requires Chat Completions or Messages compatibility.
---

# Concentrate Responses API

Use `POST https://api.concentrate.ai/v1/responses` as the default production interface. Authenticate with `Authorization: Bearer $CONCENTRATE_API_KEY` and never embed keys in source.

## Workflow

1. Confirm the requested model and required capabilities against the live model API. Do not rely on a static model list.
2. Build the smallest valid request with `model`, `input`, and an explicit `max_output_tokens` when cost or length matters.
3. Add tools, structured output, streaming, caching, or reasoning only when the selected provider supports them.
4. Parse output items by their `type`; do not assume the first array element is always text.
5. Handle non-2xx responses and terminal stream events explicitly. Log resolved model, usage, cost, and request ID where operationally appropriate.

## Read the relevant reference

- For endpoint shape, authentication, output extraction, stateful turns, and compatibility boundaries, read [references/core-api.md](references/core-api.md).
- For function tools, structured JSON, or web search, read [references/tools-structured-search.md](references/tools-structured-search.md).
- For SSE, prompt caching, retries, or failures, read [references/streaming-caching-errors.md](references/streaming-caching-errors.md).

## Guardrails

- Responses function tools use top-level `name` and `parameters`; the nested Chat Completions `function` shape is wrong here.
- Treat model/provider feature support as live data. Routing may degrade unsupported optional features, so pin or restrict a provider when a feature is mandatory.
- Guardrails, ZDR, request logging, and BYOK are key/dashboard policies, not ordinary Responses body parameters. Use `concentrate-data-controls` for those workflows.
- Chat Completions and Messages endpoints are beta compatibility layers. The official docs recommend Responses for production.
- Do not invent image-generation, audio, video, embeddings, batch, files, or fine-tuning endpoints. Only use documented surfaces.
