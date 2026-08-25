---
name: concentrate-responses
description: Generate text, code, structured JSON outputs, streaming completions, and execute tool/function calling using Concentrate AI's unified Responses API (`https://api.concentrate.ai/v1/responses`). Use when the user asks to integrate Concentrate AI, call LLMs via Concentrate, build chat/completion workflows, implement tool calling, enable SSE streaming, or request structured JSON outputs.
---

# Concentrate AI Responses API

The **Concentrate AI Responses API** (`POST https://api.concentrate.ai/v1/responses`) provides a unified, normalized interface for querying 170+ AI models across 21 providers with automatic provider fallback, prompt caching, and credit tracking.

---

## 1. Authentication & Base URL

* **Base URL:** `https://api.concentrate.ai/v1/responses`
* **Header:** `Authorization: Bearer YOUR_CONCENTRATE_API_KEY`
* **Environment Variable:** `CONCENTRATE_API_KEY` (Get keys from [concentrate.ai](https://concentrate.ai))

---

## 2. Quickstart Examples

### TypeScript / JavaScript (`fetch`)
```typescript
interface Message {
  role: "system" | "user" | "assistant" | "developer";
  content: string;
}

async function createResponse(prompt: string, model = "gpt-5.6-sol") {
  const response = await fetch("https://api.concentrate.ai/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.CONCENTRATE_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: model,
      input: prompt,
      max_output_tokens: 2048,
      temperature: 0.7
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Concentrate API error (${response.status}): ${JSON.stringify(error)}`);
  }

  const data = await response.json();
  // Extract text from normalized response
  return data.output[0].content[0].text;
}
```

### Python (`requests`)
```python
import os
import requests

def generate_response(prompt: str, model: str = "gpt-5.6-sol") -> str:
    url = "https://api.concentrate.ai/v1/responses"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CONCENTRATE_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": prompt,
        "max_output_tokens": 2048
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["output"][0]["content"][0]["text"]
```

---

## 3. Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `model` | `string` | **Yes** | Model identifier (e.g., `"gpt-5.6-sol"`, `"anthropic/claude-opus-5"`, `"auto"`). |
| `input` | `string \| array` | **Yes** | Plain string prompt OR array of conversation messages / tool call objects. |
| `text` | `object` | No | Controls output format (e.g. `json_schema` for structured outputs). |
| `tools` | `array` | No | List of function tools or `[{"type": "web_search"}]`. |
| `tool_choice` | `string \| object` | No | `"auto"`, `"none"`, `"required"`, or `{ "type": "function", "function": { "name": "..." } }`. |
| `stream` | `boolean` | No | Set `true` to stream responses via Server-Sent Events (SSE). |
| `max_output_tokens` | `integer` | No | Maximum tokens to generate. |
| `temperature` | `number` | No | Sampling temperature (0.0 to 2.0). |
| `routing` | `object` | No | Controls provider sort criteria, latency thresholds, and fallbacks. |

---

## 4. Multi-Turn Conversations

When sending conversation history, provide an array of message objects:

```json
{
  "model": "gpt-5.6-sol",
  "input": [
    {
      "role": "system",
      "content": "You are an expert full-stack developer assistant."
    },
    {
      "role": "user",
      "content": "How do I implement JWT authentication in FastAPI?"
    }
  ]
}
```

---

## 5. Structured Outputs (JSON Schema)

Force the model to return valid, type-safe JSON matching your schema:

```json
{
  "model": "gpt-5.6-sol",
  "input": "Extract user details from: Jane Doe is a 29 year old software engineer in San Francisco.",
  "text": {
    "format": {
      "type": "json_schema",
      "name": "user_profile",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "age": { "type": "integer" },
          "occupation": { "type": "string" },
          "city": { "type": "string" }
        },
        "required": ["name", "age", "occupation", "city"],
        "additionalProperties": false
      }
    }
  }
}
```

---

## 6. Tool / Function Calling

### Defining Tools
```json
{
  "model": "gpt-5.6-sol",
  "input": "What's the weather in Tokyo?",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get current weather conditions for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": { "type": "string", "description": "City and country" },
            "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
          },
          "required": ["location"]
        }
      }
    }
  ]
}
```

### Multi-Turn Tool Resolution Loop
When the model returns a `function_call`, append the call and its `function_call_output` to `input`:

```json
{
  "model": "gpt-5.6-sol",
  "input": [
    { "role": "user", "content": "What's the weather in Tokyo?" },
    {
      "type": "function_call",
      "call_id": "call_tokyo_123",
      "name": "get_current_weather",
      "arguments": "{\"location\": \"Tokyo\", \"unit\": \"celsius\"}"
    },
    {
      "type": "function_call_output",
      "call_id": "call_tokyo_123",
      "output": "{\"temperature\": 18, \"condition\": \"Partly Cloudy\"}"
    }
  ]
}
```

---

## 7. Real-Time Streaming (SSE)

Send `"stream": true` and read Server-Sent Events chunks:

```typescript
const response = await fetch("https://api.concentrate.ai/v1/responses", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.CONCENTRATE_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gpt-5.6-sol",
    input: "Explain quantum computing simply",
    stream: true
  })
});

const reader = response.body?.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader!.read();
  if (done) break;
  const chunk = decoder.decode(value);
  // Process SSE lines starting with 'data: '
  const lines = chunk.split("\n").filter(l => l.startsWith("data: "));
  for (const line of lines) {
    const jsonStr = line.replace("data: ", "").trim();
    if (jsonStr === "[DONE]") return;
    const data = JSON.parse(jsonStr);
    if (data.delta?.text) {
      process.stdout.write(data.delta.text);
    }
  }
}
```

---

## 8. Built-in Web Search Tool

Enable live internet searching directly:
```json
{
  "model": "gpt-5.6-sol",
  "input": "What were the latest AI breakthroughs announced this week?",
  "tools": [
    { "type": "web_search" }
  ]
}
```
