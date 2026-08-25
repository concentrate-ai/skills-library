---
name: concentrate-multimodal
description: Send and troubleshoot image inputs through Concentrate AI for vision analysis, OCR, screenshots, diagrams, receipts, and multi-image comparison. Use for Responses API input images; do not use for image generation or editing, which Concentrate does not currently document.
---

# Concentrate Multimodal Inputs

Use the Responses API with `input_text` and `input_image` content blocks. Concentrate normalizes public image URLs and base64 data URIs across vision-capable providers.

## Workflow

1. Query the live catalog for image-capable models. Prefer `concentrate-models` or its bundled script.
2. Inspect `GET /v1/models/{model}` for each intended provider's formats, count, size, and resolution limits.
3. Choose URL input only when the URL is public and stable; otherwise encode the local file as a correctly typed data URI.
4. Add multiple image blocks only within the selected provider's limits.
5. Treat `detail` as provider-dependent and default to `auto` unless the use case and provider justify `low` or `high`.
6. Handle validation errors without blindly retrying the same payload.

Read [references/image-inputs.md](references/image-inputs.md) for the request shape, capability fields, provider-dependent limits, and errors.

## Boundaries

- Supported formats in the general API do not guarantee every provider accepts every format.
- A model family commonly associated with vision is not proof that the selected provider route supports images.
- Higher resolution can increase token use and cost.
- Do not claim support for audio input, speech, video, image generation, or image editing unless the official Concentrate docs add those surfaces.
