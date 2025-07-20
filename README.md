## Panaversity AI Assistant — Quickstart Guide

This guide walks you through the logical blocks of building a Chainlit-powered AI assistant using Gemini via an OpenAI-compatible interface.

---

### 1. Environment Setup

First, load your environment variables to keep sensitive data (like `GEMINI_API_KEY`) secure:

```python
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
```

**Why?**  
- Keeps API keys out of your codebase.
- Stops execution early if config is missing.

---

### 2. Import Chainlit & Agents SDK

Bring in the required libraries and SDKs:

```python
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
```

**Key Components:**  
- `chainlit`: Chat UI frontend  
- `Agent`: Represents your LLM agent  
- `Runner`: Executes the agent  
- `AsyncOpenAI`: Gemini wrapper  
- `OpenAIChatCompletionsModel`: Model interface  
- `RunConfig`: Configuration holder

---

### 3. Session Initialization (`@cl.on_chat_start`)

Set up the session when a user connects:

```python
@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    cl.user_session.set("agent", agent)
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()
```

**What happens?**  
- Initializes Gemini via OpenAI wrapper  
- Stores config, agent, and chat history in session  
- Sends a welcome message

---

### 4. Message Handling (`@cl.on_message`)

Process each user message:

```python
@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    result = Runner.run_sync(
        starting_agent=agent,
        input=history,
        run_config=config
    )
    response_content = result.final_output
    msg.content = response_content
    await msg.update()
    cl.user_session.set("chat_history", result.to_input_list())
    print(f"User: {message.content}")
    print(f"Assistant: {response_content}")
except Exception as e:
    msg.content = f"Error: {str(e)}"
    await msg.update()
```

**Why this flow?**  
- Shows "Thinking..." for responsiveness  
- Retrieves agent/config from session  
- Maintains chat history for context  
- Updates message with LLM reply  
- Handles errors gracefully

---

### 🧠 Key Concepts

| Concept                | Why It Matters                                      |
|------------------------|-----------------------------------------------------|
| Session state          | Tracks config, agent, and history per user          |
| Agent object           | The LLM and its instructions                        |
| `Runner.run_sync(...)` | Runs the agent with full history                    |
| History handling       | Gives the assistant memory                          |
| Async message updates  | Keeps chat responsive and interactive               |

---

You're now ready to build and extend your own Chainlit-powered AI assistant!
