# Tools, structured output, and web search

Official sources: [Tool Calling](https://concentrate.ai/docs/api-reference/endpoint/tool-calling), [Structured Output](https://concentrate.ai/docs/api-reference/endpoint/structured-output), and [Web Search](https://concentrate.ai/docs/api-reference/endpoint/web-search).

Before using a feature, inspect `GET /v1/models/{model}` and confirm at least one intended provider reports support for it.

## Function tools

Responses tools put `name`, `description`, and `parameters` directly on the tool object. Do not use the Chat Completions-style nested `function` object.

```json
{
  "model": "gpt-4o",
  "input": "What is the weather in Pune?",
  "tools": [
    {
      "type": "function",
      "name": "get_weather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": { "type": "string" }
        },
        "required": ["location"],
        "additionalProperties": false
      },
      "strict": true
    }
  ],
  "tool_choice": "auto"
}
```

Tool names must match `^[a-zA-Z0-9_.-]+$`. Strict mode defaults to true; strict schemas must include `additionalProperties: false`.

Handle every returned `function_call`, parse its JSON-string `arguments`, execute only authorized application code, and return a matching `function_call_output`:

```json
{
  "type": "function_call_output",
  "call_id": "call_abc123",
  "output": "{\"temperature_c\": 24}",
  "is_error": false
}
```

Include the original `function_call` item and its output in the next `input`. Enable `parallel_tool_calls` only when calls are independent.

## Structured output

```json
{
  "model": "gpt-4o",
  "input": "Extract the name and age: Mira is 31.",
  "text": {
    "format": {
      "type": "json_schema",
      "name": "person",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "age": { "type": "integer" }
        },
        "required": ["name", "age"],
        "additionalProperties": false
      }
    }
  }
}
```

Parse the returned output text as JSON and validate it in the application even when strict mode is requested. Routing may degrade unsupported features; pin or restrict providers when schema enforcement is a hard requirement.

## Web search

Use the built-in web-search tool only as documented on the official web-search page and confirm provider capability first. Preserve citation annotations returned in message content instead of manufacturing citations from plain text.
