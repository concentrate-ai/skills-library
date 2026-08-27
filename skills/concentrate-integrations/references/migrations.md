# Gateway migrations

Official source: [Migrations overview](https://concentrate.ai/docs/migrations/overview).

Concentrate publishes focused migration guides for:

- [OpenRouter](https://concentrate.ai/docs/migrations/openrouter)
- [Helicone](https://concentrate.ai/docs/migrations/helicone)
- [Portkey](https://concentrate.ai/docs/migrations/portkey)
- [Merge](https://concentrate.ai/docs/migrations/merge)
- [Vercel AI Gateway](https://concentrate.ai/docs/migrations/vercel)
- [TensorZero](https://concentrate.ai/docs/migrations/tensorzero)
- [LiteLLM](https://concentrate.ai/docs/migrations/litellm)

## Migration method

1. Identify whether the current application calls a proxy, an imported SDK, or a provider-native endpoint.
2. Read the matching official migration guide before changing code. Each source has different headers, routing concepts, model identifiers, and unsupported features.
3. Replace the base URL and key only where the source is OpenAI-compatible. SDK-only abstractions may need direct client replacement.
4. Replace source-specific model aliases with live Concentrate bare slugs or serving-provider-prefixed slugs.
5. Map routing, fallbacks, budgets, observability, and metadata separately; a base-URL swap does not migrate every gateway feature.
6. Test non-streaming, streaming, tools, structured output, errors, resolved model/provider, and cost reporting before cutting over.
7. Export historical logs from the previous gateway when retention or audit needs require them; histories do not automatically transfer.

## Important gaps

Do not imply feature parity where the source guide says there is none. Examples documented across migration guides include source-specific headers, aliases, tags, config files, callback integrations, and self-hosted control planes. Concentrate generally attributes usage through its organization/team/developer/key hierarchy rather than arbitrary per-request gateway tags.

For new application code, the official guides recommend adopting the native Responses API after compatibility migration is stable.
