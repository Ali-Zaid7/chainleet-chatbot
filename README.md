# Panaversity AI Assistant — Quickstart Guide

This guide walks you through setting up and running a Gemini-powered chatbot using Chainlit and Agents SDK.

---

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Importing Dependencies](#importing-dependencies)
3. [Session Initialization](#session-initialization)
4. [Message Handling](#message-handling)
5. [Key Concepts](#key-concepts)

---

## 1. Environment Setup

First, load your environment variables securely:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
```

> **Note:** Never hardcode sensitive data like API keys.

---

## 2. Importing Dependencies

Import Chainlit and Agents SDK modules:

```python
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
```

- `chainlit`: Manages the chat UI frontend.
- `Agent`: Represents the LLM agent.
- `Runner`: Executes the agent.
- `AsyncOpenAI`: Gemini API wrapper (OpenAI-compatible).
- `OpenAIChatCompletionsModel`: Standard model interface.
- `RunConfig`: Holds agent configuration.

---

## 3. Session Initialization

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

---

## 4. Message Handling

Process each user message and respond:

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
```

Handle errors gracefully:

```python
except Exception as e:
    msg.content = f"Error: {str(e)}"
    await msg.update()
```

---

## 5. Key Concepts

| Concept                       | Why It's Important                                      |
|-------------------------------|--------------------------------------------------------|
| Session state (`cl.user_session`) | Tracks config, agent, and history per user            |
| Agent object                  | The LLM and its instructions ("the brain")             |
| `Runner.run_sync(...)`        | Runs the agent using all chat history                  |
| History handling              | Gives memory to the assistant (LLMs are stateless)     |
| Async message updates         | Keeps chat responsive ("Thinking..." → reply)          |

---

**You're ready to build and extend your own Gemini-powered chatbot!**
