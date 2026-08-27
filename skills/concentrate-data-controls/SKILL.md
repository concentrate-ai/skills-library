---
name: concentrate-data-controls
description: Configure and reason about Concentrate AI Zero Data Retention, request logging, PII redaction guardrails, the redact-v1 model, and Bring Your Own Key routing. Use for privacy, compliance, sensitive data, retention, provider credentials, or BYOK billing questions.
---

# Concentrate Data Controls

Treat ZDR, logging, guardrails, and BYOK as dashboard/key-scope controls. They are not ordinary per-request switches. Keep distinct what Concentrate stores, what upstream providers retain, what is redacted, and whose provider credential is billed.

## Workflow

1. Identify the requirement: upstream retention, Concentrate request logging, PII redaction, provider ownership/billing, or a combination.
2. Determine the policy scope (organization, team, user, or key) and whether a higher-level policy locks the setting.
3. For ZDR, inspect the exact model/provider pair in `GET /v1/models/{model}`. Only a provider whose `zdr` value is an object qualifies.
4. For guardrails, account for the output-streaming limitation and configure at least one entity type before using `redact-v1`.
5. For BYOK, configure credentials in the dashboard and verify `cost.byok` in responses rather than adding custom request headers.
6. Explain remaining metadata collection and fallback behavior accurately; do not imply that any one control eliminates every form of operational metadata.

## Read the relevant reference

- For ZDR, logging, enforcement hierarchy, and strict 422 behavior, read [references/zdr-and-logging.md](references/zdr-and-logging.md).
- For guardrails, `redact-v1`, BYOK setup semantics, billing, and fallback, read [references/redaction-and-byok.md](references/redaction-and-byok.md).

## Boundaries

- ZDR is a property of a model/provider pair, not a model author or model name.
- A provider prefix alone does not enable key-level ZDR enforcement; configure ZDR on the key when the strict policy is required.
- Output redaction does not apply to streamed responses.
- BYOK keys are dashboard-managed, encrypted, write-only credentials. Never request that users paste them into source code or skill files.
- Do not make legal, HIPAA, GDPR, or audit-certification claims beyond what the official policies and the user's compliance team establish.
