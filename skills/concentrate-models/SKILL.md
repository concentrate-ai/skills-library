---
name: concentrate-models
description: Discover and compare live Concentrate AI models and providers, check capabilities, pricing, limits, ZDR, and deprecations, and configure provider/model routing and fallbacks. Use when model choice or route behavior matters; never rely on a static catalog for current availability.
---

# Concentrate Models and Routing

Query the live public catalog before recommending or configuring a model. Model names, providers, pricing, capabilities, and counts change over time.

## Use the bundled script

The dependency-free script calls only public catalog endpoints:

```bash
python3 <skill-path>/scripts/concentrate_models.py list --search claude
python3 <skill-path>/scripts/concentrate_models.py list --capability input.image --sort context
python3 <skill-path>/scripts/concentrate_models.py show gpt-4o
python3 <skill-path>/scripts/concentrate_models.py compare gpt-4o claude-sonnet-4-6
python3 <skill-path>/scripts/concentrate_models.py providers
```

Use `--json` when another program or agent needs the raw output. No API key is required.

## Workflow

1. Turn the user's needs into concrete constraints: input type, tools, structured output, reasoning, context, output limit, data policy, provider, price, or latency.
2. Search the live list, then inspect each candidate with `show` for provider-specific details.
3. If ZDR is required, accept only provider entries whose `zdr` value is an object; a model-level name alone is not proof of ZDR.
4. Choose a bare slug when provider flexibility is useful, a `provider/model` prefix when the initial provider matters, or `auto` only with the documented limitation that model-based optimization is currently simplified.
5. Configure provider sorting and model/provider fallbacks explicitly when resilience or optimization matters.
6. Present the observed live data and the selection tradeoff, not an unsupported universal ranking.

Read [references/catalog-routing.md](references/catalog-routing.md) for endpoints, filters, identifier semantics, routing, fallback, and feature-degradation behavior.

## Boundaries

- Provider prefixes pin the first route but documented fallback may still move to another provider for the same model.
- `routing.provider.fallbacks` is a whitelist of eligible providers.
- Do not copy model tables into generated code or skill instructions when a live query will work.
- Do not infer image, PDF, tool, structured-output, reasoning, caching, or ZDR support from a model family name.
- Do not claim an OpenRouter-style benchmark, generation-history, analytics, or dedicated SDK API; Concentrate does not document those surfaces.
