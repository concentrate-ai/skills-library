# Image inputs

Official source: [Multi-Modal Inputs](https://concentrate.ai/docs/api-reference/endpoint/multi-modal).

## Request shape

Send `input_image` beside `input_text` in a message content array:

```json
{
  "model": "gpt-4o",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_text", "text": "Describe this image." },
        {
          "type": "input_image",
          "image_url": "https://example.com/photo.png",
          "detail": "auto"
        }
      ]
    }
  ]
}
```

`image_url` may be a public HTTPS URL or a base64 data URI. Public URLs must be reachable without authentication. Multiple `input_image` blocks are allowed within provider limits.

Supported documented formats are PNG, JPEG, GIF, and WebP, but individual providers may support only a subset. Match the data-URI MIME type to the actual bytes.

## Capability and limits

Treat live catalog data as authoritative:

- `GET /v1/models` → `capabilities.image_input.supported`
- `GET /v1/models/{model}` → provider `supports.input.image` and `image_processing`

Provider detail may expose supported formats, maximum images per request, maximum total size, `max_pixels`, and `max_dimension`. Validate against the exact provider route. If the route is flexible, satisfy the strictest eligible provider limit or pin a known-compatible provider.

The official guide documents different limits for OpenAI, Anthropic, Vertex model families, Cohere, and Mistral. Do not freeze those numbers into application logic; query model detail before validation because limits change by model/provider.

## Detail control

`detail` accepts `low`, `high`, or `auto`, but not every provider has a native equivalent. OpenAI, xAI, Cohere, Mistral, and some Azure routes accept or map it; Anthropic, Vertex, Bedrock, and Z.AI routes may decide resolution themselves. Do not promise that `detail: "high"` changes behavior on every route.

## Errors

Handle 400 errors for unsupported image input, excessive image count/size/resolution, invalid formats, and invalid URLs. Resize or convert locally rather than retrying an unchanged invalid payload.

This is image **input** for vision analysis. It is not an image-generation or editing API.
