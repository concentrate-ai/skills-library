---
name: concentrate-integrations
description: Configure AI developer tools (Claude Code, Cursor, Codex CLI, Claude Desktop) and OpenAI/Anthropic SDKs to use Concentrate AI as the backend LLM provider. Use when the user asks how to use Concentrate in Cursor, Claude Code, Python OpenAI SDK, or LangChain/LlamaIndex.
---

# Concentrate AI Tool & SDK Integrations

Concentrate AI offers full compatibility layers for **Anthropic Messages** (`/v1/messages`) and **OpenAI Chat Completions** (`/v1/chat/completions`), allowing you to plug Concentrate directly into your existing developer tools and SDKs without refactoring code.

---

## 1. Claude Code Setup

Use Claude Code with any model on Concentrate (including DeepSeek, MiniMax, GLM, Kimi, GPT-5.6, Gemini 3.6, and Claude) on a pay-as-you-go basis.

### Quick Setup (CLI)
Set the Anthropic base URL and your Concentrate API key in your shell:

```bash
export ANTHROPIC_BASE_URL="https://api.concentrate.ai/v1"
export ANTHROPIC_API_KEY="YOUR_CONCENTRATE_API_KEY"
```

Then run Claude Code normally:
```bash
claude
```

### Persistent Configuration
Add the export lines to your `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export ANTHROPIC_BASE_URL="https://api.concentrate.ai/v1"' >> ~/.zshrc
echo 'export ANTHROPIC_API_KEY="YOUR_CONCENTRATE_API_KEY"' >> ~/.zshrc
source ~/.zshrc
```

---

## 2. Cursor Setup

Configure Cursor to use Concentrate's 170+ models via OpenAI-compatible endpoints:

1. Open **Cursor Settings** (`Cmd + Shift + J` on Mac or `Ctrl + Shift + J` on Windows/Linux).
2. Navigate to **Models** in the sidebar.
3. Under **OpenAI API Key**:
   * Toggle **Override OpenAI Base URL** $\to$ **ON**.
   * Set Base URL to: `https://api.concentrate.ai/v1`
   * Enter your Concentrate API Key in the **OpenAI API Key** field.
4. Add your desired models under **Model Names** (e.g. `gpt-5.6-sol`, `claude-opus-5`, `gemini-3.6-flash`, `deepseek-v4-pro`).

---

## 3. OpenAI SDK Compatibility (Python & TypeScript)

If you have existing code using the official `openai` package, change only the `base_url` and `api_key`:

### Python (`openai` package)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.concentrate.ai/v1",
    api_key=os.environ.get("CONCENTRATE_API_KEY")
)

response = client.chat.completions.create(
    model="gpt-5.6-sol", # or "anthropic/claude-opus-5", "deepseek-v4-pro"
    messages=[
        {"role": "system", "content": "You are a senior systems architect."},
        {"role": "user", "content": "Explain event-driven architecture."}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

### TypeScript / Node.js (`openai` npm package)
```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  baseURL: "https://api.concentrate.ai/v1",
  apiKey: process.env.CONCENTRATE_API_KEY
});

async function run() {
  const completion = await openai.chat.completions.create({
    model: "claude-opus-5",
    messages: [
      { role: "user", content: "Write a high-performance LRU cache in TypeScript." }
    ]
  });

  console.log(completion.choices[0].message.content);
}

run();
```

---

## 4. LangChain & LlamaIndex Compatibility

### LangChain (Python)
```python
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://api.concentrate.ai/v1",
    api_key=os.environ.get("CONCENTRATE_API_KEY"),
    model="gpt-5.6-sol"
)

result = llm.invoke("Summarize microservices best practices.")
print(result.content)
```

### LlamaIndex (Python)
```python
import os
from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    api_base="https://api.concentrate.ai/v1",
    api_key=os.environ.get("CONCENTRATE_API_KEY"),
    model="gemini-3.6-flash",
    is_chat_model=True
)

response = llm.complete("What are vector embeddings?")
print(response.text)
```
