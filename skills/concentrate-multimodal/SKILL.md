---
name: concentrate-multimodal
description: Send images and multimodal inputs alongside text prompts to vision-capable models on Concentrate AI. Use when the user asks to analyze images, perform OCR, inspect screenshots/diagrams, parse receipts/documents, or process visual data with models like GPT-5.6, Claude Opus 5, Gemini 3.6 Flash, or Qwen VL.
---

# Concentrate AI Multi-Modal & Vision Inputs

Concentrate AI allows you to send images (via public HTTPS URLs or base64 data URIs) alongside text to **100+ vision-capable models** using a normalized interface.

---

## 1. Supported Vision Models

| Author | Recommended Vision Models |
| :--- | :--- |
| **OpenAI** | `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.5`, `gpt-5.4`, `gpt-4o` |
| **Anthropic** | `claude-fable-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5` |
| **Google** | `gemini-3.6-flash`, `gemini-3.1-pro-preview`, `gemini-2.5-pro` |
| **Alibaba** | `qwen3-vl-plus`, `qwen3.8-max`, `qwen3-vl-235b-a22b` |
| **xAI** | `grok-4.5`, `grok-4.3`, `grok-build-0.1` |
| **Meta** | `llama-4-maverick`, `llama-4-scout` |

---

## 2. Image Input Format

Images are passed as `input_image` blocks inside the message `content` array:

```json
{
  "model": "gpt-5.6-terra",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is depicted in this image, and what are the main architectural elements?"
        },
        {
          "type": "input_image",
          "image_url": "https://example.com/architecture-plan.jpg",
          "detail": "high"
        }
      ]
    }
  ]
}
```

### Properties
* `type` (required): `"input_image"`
* `image_url` (required): Public HTTPS URL or Base64 Data URI (`data:image/jpeg;base64,...`)
* `detail` (optional): `"low"`, `"high"`, or `"auto"` (default: `"auto"`)
  * `low`: Lower token cost, faster processing.
  * `high`: Full resolution inspection.
  * `auto`: Automatic determination.

---

## 3. Code Examples

### TypeScript / JavaScript (Base64 Local Image)
```typescript
import * as fs from "fs";

async function analyzeLocalImage(imagePath: string, prompt: string) {
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Data = imageBuffer.toString("base64");
  const mimeType = imagePath.endsWith(".png") ? "image/png" : "image/jpeg";
  const dataUri = `data:${mimeType};base64,${base64Data}`;

  const response = await fetch("https://api.concentrate.ai/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.CONCENTRATE_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-5.6-sol",
      input: [
        {
          "role": "user",
          "content": [
            { "type": "input_text", "text": prompt },
            { "type": "input_image", "image_url": dataUri, "detail": "high" }
          ]
        }
      ]
    })
  });

  const result = await response.json();
  return result.output[0].content[0].text;
}
```

### Python (Public Image URL)
```python
import os
import requests

def inspect_image_url(image_url: str, question: str, model: str = "gemini-3.6-flash") -> str:
    url = "https://api.concentrate.ai/v1/responses"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CONCENTRATE_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": question},
                    {"type": "input_image", "image_url": image_url, "detail": "auto"}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["output"][0]["content"][0]["text"]
```

---

## 4. Multi-Image Comparisons

You can pass multiple `input_image` blocks within the same message or turn:

```json
{
  "model": "claude-opus-5",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_text", "text": "Compare these two UI wireframes and point out differences in navigation." },
        { "type": "input_image", "image_url": "https://example.com/v1.png" },
        { "type": "input_image", "image_url": "https://example.com/v2.png" }
      ]
    }
  ]
}
```
