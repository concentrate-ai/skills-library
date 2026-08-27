# Core Responses API

Official sources: [Create Response](https://concentrate.ai/docs/api-reference/endpoint/create-response), [Request Parameters](https://concentrate.ai/docs/api-reference/endpoint/request-parameters), and [OpenAPI](https://concentrate.ai/docs/api-reference/openapi.json).

## Endpoint and authentication

```text
POST https://api.concentrate.ai/v1/responses
Authorization: Bearer $CONCENTRATE_API_KEY
Content-Type: application/json
```

`model` and `input` are required. `input` may be a string or an array of messages and tool items. Message roles are `user`, `assistant`, `system`, and `developer`.

```bash
curl https://api.concentrate.ai/v1/responses \
  -H "Authorization: Bearer $CONCENTRATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "input": "Explain this API in one sentence.",
    "max_output_tokens": 200
  }'
```

Set `max_output_tokens` explicitly for predictable cost and response length. Do not assume every model/provider supports every optional parameter; inspect the live model detail before relying on a feature.

## Output

Text is normally found in an output item with `type: "message"`, then in a content part with `type: "output_text"`. Iterate by `type`; do not assume the desired text is always at array index zero because reasoning and tool-call items may also appear.

```javascript
function outputText(response) {
  return response.output
    .filter((item) => item.type === "message")
    .flatMap((item) => item.content ?? [])
    .filter((part) => part.type === "output_text")
    .map((part) => part.text)
    .join("");
}
```

The response also reports resolved `model`, `usage`, and `cost`; log those fields when routing or spend matters.

## Stateful turns

The Responses API supports `previous_response_id` for server-managed conversation continuity when the selected provider supports it. Otherwise, send the relevant prior message and tool items again in `input`. Verify provider support through `GET /v1/models/{model}` rather than assuming all routes support conversation state.

## Compatibility endpoints

- `POST /v1/chat/completions` is an OpenAI Chat Completions compatibility endpoint in beta.
- `POST /v1/messages` is an Anthropic Messages compatibility endpoint in beta.
- Official docs recommend the Responses API for production.

Use compatibility endpoints only when a client requires their native shape. Do not mix their tool schemas with the Responses schema.
