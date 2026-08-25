---
name: concentrate-integrations
description: Connect supported clients to Concentrate AI and migrate from OpenRouter, Helicone, Portkey, Merge, Vercel AI Gateway, TensorZero, or LiteLLM. Use for Claude Code, Claude Desktop, Cursor, OpenAI-compatible clients, compatibility endpoints, base URLs, or gateway migration; flag Codex as currently nonfunctional per official docs.
---

# Concentrate Integrations and Migrations

Choose configuration from the client's protocol, not its branding. OpenAI-compatible tools use the `/v1` base URL; Anthropic-native tools use the host without `/v1` because they append it themselves.

## Workflow

1. Identify the client's wire protocol and whether its Concentrate integration is documented as stable, beta, or unsupported.
2. Query the live model catalog and any integration-compatibility fields before selecting a model.
3. Configure the documented base URL and a Concentrate key without exposing it in source or logs.
4. Keep the client's native request schema. Compatibility does not make Responses, Chat Completions, and Messages tool formats interchangeable.
5. Verify endpoint, auth, exact model slug, one non-streamed request, and usage in the dashboard.
6. For migrations, read the source-specific guide and map non-API concerns such as routing, budgets, tags, logs, and fallbacks explicitly.

## Read the relevant reference

- For base URLs, Claude Code, Claude Desktop, Cursor, Codex status, and beta endpoints, read [references/clients.md](references/clients.md).
- For gateway migration procedure and documented source guides, read [references/migrations.md](references/migrations.md).

## Boundaries

- Do not configure Anthropic-native tools with `https://api.concentrate.ai/v1`; that can create `/v1/v1` paths.
- Do not claim Codex currently works; the official page says it is unsupported and nonfunctional.
- Do not claim a dedicated Concentrate SDK. Use documented HTTP compatibility or established client libraries with configurable base URLs.
- Do not claim integrations for LangChain, LlamaIndex, or other clients unless the current official docs substantiate the exact configuration, or clearly present it as an inferred generic OpenAI-compatible pattern.
