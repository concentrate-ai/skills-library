# Streaming, caching, and errors

Official sources: [Streaming](https://concentrate.ai/docs/api-reference/endpoint/streaming), [Prompt Caching](https://concentrate.ai/docs/api-reference/endpoint/prompt-caching), and [Errors](https://concentrate.ai/docs/api-reference/endpoint/errors).

## Streaming

Set `stream: true` and parse Server-Sent Events. Buffer across network chunks; a chunk boundary is not an event boundary. Read both the `event:` and `data:` lines when present.

The primary text event is `response.output_text.delta`. Terminal events include `response.completed`, `response.failed`, `response.incomplete`, and `error`. Tool argument events are `response.function_call_arguments.delta` and `.done`.

Provider fallback for streaming can occur only before the stream begins. Once bytes are emitted, the request is committed to that provider.

## Prompt caching

Caching controls are provider-specific:

- Direct OpenAI GPT-5.6 routes use request-level `prompt_cache_options` and block-level `prompt_cache_breakpoint`.
- Anthropic and AWS Bedrock Claude routes use `cache_control` with `ttl: "5m"` or `"1h"`.
- Concentrate documents cross-provider conversion between these marker styles, with provider-specific TTL rounding and marker limits.

Put stable prompt prefixes first. Confirm cache activity with `usage.input_tokens_details.cached_tokens` and `cache_write_tokens`; do not add these detail counters to `input_tokens`.

Read the official prompt-caching guide before implementing explicit markers because supported models, TTL conversion, and write limits are provider-dependent.

## Error handling

Handle the documented statuses:

| Status | Meaning | Typical action |
|---|---|---|
| 400 | Invalid request | Fix schema or unsupported values; do not retry unchanged |
| 401 | Invalid authentication | Fix the key; do not retry unchanged |
| 402 | Insufficient credits | Add funds or use a valid BYOK route |
| 422 | ZDR has no eligible route | Choose a ZDR-capable model/provider or change key policy |
| 424 | Providers exhausted/failed | Retry with bounded backoff or broader fallbacks |
| 429 | Rate limited | Honor `Retry-After` when present |
| 500, 503 | Server/service failure | Retry with exponential backoff and jitter |
| 504 | Upstream timeout | Retry cautiously; the upstream may have partially processed it |

Set client timeouts. Bound retries. Do not blindly retry non-idempotent tool work. Preserve `X-Request-Id` and the response error body for support.
