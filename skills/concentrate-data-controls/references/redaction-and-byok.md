# Redaction guardrails and BYOK

Official sources: [Guardrails and PII redaction](https://concentrate.ai/docs/api-reference/endpoint/guardrails-redaction) and [Bring Your Own Key](https://concentrate.ai/docs/api-reference/endpoint/byok).

## Guardrails

Configure redaction for a key in the dashboard with target `input`, `output`, or `both`, plus the selected entity types.

- Input redaction occurs before model processing.
- Output redaction occurs before a non-streamed response is returned.
- Streamed output is not redacted.

`redact-v1` (aliases `redact` and `concentrate-redact`) uses `/v1/responses` to return scrubbed input without forwarding it to an upstream LLM:

```json
{
  "model": "redact-v1",
  "input": "Email jane@example.com about invoice 4823"
}
```

The calling key must already have guardrails enabled with at least one entity type, or the request fails with 400. The key's entity types, placeholder, and confidence threshold apply; its target setting is ignored for this model because the model always returns redacted input. Extract redacted text from the normal output message and inspect the attached `redact` summary when needed.

## BYOK

BYOK credentials are stored once in the dashboard at personal or organization scope. Every Concentrate API key in that scope can use them automatically; there is no per-request opt-in.

Routing prefers otherwise-equal providers for which the scope has BYOK credentials. It tries stored keys for that provider, then Concentrate's credential for that provider, then the next provider. A bad BYOK key does not by itself fail the request.

When served through BYOK:

- Concentrate does not debit credits and its rate limit does not apply.
- The upstream provider bills the owner and enforces its limits.
- Concentrate still tracks usage and observability.
- `cost.byok` is `true` and `cost.total` is zero.

Most providers accept one key string. Azure requires resource metadata, Vertex requires service-account JSON and permissions, and Bedrock accepts a Bedrock key or AWS credentials plus region. Follow the official BYOK page for current credential fields and never reproduce real credentials in output.
