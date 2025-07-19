# 🤖 Gemini Agent Integration with OpenAI-Compatible Agents SDK

This repo/Colab notebook is a self-practice project to integrate **Google Gemini API** with the **OpenAI-compatible `agents` SDK**. It supports both asynchronous and synchronous flows, custom environment configuration, and flexible agent-level setup.

---

## 📌 Objective

- Use **Google Gemini (via OpenAI-compatible wrapper)** inside the `agents` library.
- Learn different ways to **run agents**, configure **model providers**, and handle **authentication**.
- Understand how to use:
    - `.env` + fallback system
    - `AsyncOpenAI` vs `OpenAI`
    - `Runner.run` vs `Runner.run_sync`
    - Agent-level model injection
    - SDK-wide defaults

---

## 🧠 Core Concepts & Recap

### 1. ✅ `.env` + Fallback Pattern

Store secrets safely in `.env`, but allow hardcoded fallback for testing.

```python
from dotenv import load_dotenv
import os

load_dotenv()
userdata = {"GEMINI_API_KEY": "your_fallback_key"}

BASE_URL = os.getenv("BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY") or userdata.get("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME") or "gemini-2.0-flash"

if not BASE_URL or not API_KEY or not MODEL_NAME:
        raise ValueError("BASE_URL, API_KEY, and MODEL_NAME must be set.")
```

> 🔒 **Best Practice:** Use `.env` in production, fallback only in notebooks.

---

### 2. 🧩 Model Client Initialization (Async Gemini)

Use `AsyncOpenAI`, compatible with OpenAI SDK but targeted to Gemini's API.

```python
from agents import AsyncOpenAI, set_tracing_disabled

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)  # Clean output, no trace logs
```

---

### 3. 🧠 Agent Definition with Model

Inject the custom Gemini model into an agent.

```python
from agents import Agent, OpenAIChatCompletionsModel

agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
)
```

> 📌 The `OpenAIChatCompletionsModel` lets Gemini act like an OpenAI ChatModel.

---

### 4. ⚙️ Running the Agent (Asynchronous)

Ideal for event-driven, streaming, or multi-tasked environments.

```python
import asyncio
from agents import Runner

async def main():
        result = await Runner.run(agent, "What is the meaning of life?")
        print(result.final_output)

if __name__ == "__main__":
        asyncio.run(main())
```

- `Runner.run`: used for asynchronous execution.

---

### 5. 🔁 (Optional) Setting Global SDK Defaults

Avoid passing model & client repeatedly:

```python
from agents import set_default_openai_client, set_default_openai_api

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api(
        "chat.completions",
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY
)
```

---

### 6. 🧵 Synchronous Alternative

If async is not required, use `run_sync`:

```python
result = Runner.run_sync(agent=agent, input="Hello")
print(result.final_output)
```

> 💡 Simpler for scripts that don’t need async I/O.

---

## 🧪 How to Test

Try these one at a time:

- ✅ Test `.env` with and without fallback
- ✅ Run `asyncio.run(main())`
- ✅ Replace `Runner.run` with `Runner.run_sync`
- ✅ Try different model instructions (e.g. "Answer only in emojis")

---

## 📚 Summary Table

| Feature                | Description                                 |
|------------------------|---------------------------------------------|
| `.env` + fallback      | Secure and testable credential setup        |
| `AsyncOpenAI`          | Connect Gemini in async OpenAI-compatible mode |
| `Agent(..., model=...)`| Custom model injection per agent            |
| `Runner.run`           | Asynchronous execution                      |
| `Runner.run_sync`      | Synchronous execution                       |
| `set_default_*`        | Global defaults for models and clients      |

---

## ✅ Final Checklist

Before you re-run after a break:

- Is `.env` file present?
- Is fallback userdata key working?
- Are `BASE_URL`, `API_KEY`, and `MODEL_NAME` initialized?
- Are you using `Runner.run` (async) or `run_sync` (sync) properly?
- Does the agent have a model assigned?

---

## 📎 Reference URLs

- 📘 [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- 🧪 [Agents SDK](https://github.com/openai/openai-python) (with agents)
- 📄 OpenAI-compatible Gemini wrapper: via any compatible proxy or plugin

---

## 🛠️ Improvements to Try Later

- Add `function_tool` calls for tool use
- Add `run_streamed()` for real-time output
- Deploy to FastAPI or Gradio UI

---

## 👋 Author

Abu-Turab – Self-learning agent SDKs with Gemini in real-world LLM orchestration.

---

## 🚦 Runner Methods Comparison

| Method                  | Blocking? | Needs `await`? | Use in `async def`? |
| ----------------------- | --------- | -------------- | ------------------- |
| `Runner.run_sync(...)`  | Yes       | No             | Optional            |
| `await Runner.run(...)` | No        | Yes            | Required            |

- **`Runner.run`**: Asynchronous — program does not block and can move to other agents to complete its task.
- **`Runner.run_sync`**: Synchronous — program blocks and waits for agent to complete its task.
- **`Runner.run_streamed`**: Asynchronous — starts streaming output.
