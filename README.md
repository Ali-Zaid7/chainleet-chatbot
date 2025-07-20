# Panaversity AI Assistant

Welcome to the Panaversity AI Assistant! This guide will walk you through the setup and usage of the assistant, which leverages the Gemini API via an OpenAI-compatible interface.

---

## 🧱 1. Environment Setup

To begin, ensure your environment is properly configured.

```python
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Access the GEMINI_API_KEY securely
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
```

### Key Notes:
- `os`: Accesses environment variables.
- `load_dotenv()`: Loads variables from a `.env` file into the environment.
- `os.getenv()`: Safely fetches the `GEMINI_API_KEY`.
- `raise ValueError(...)`: Stops execution early if a required configuration is missing.

---

## 🧠 2. Importing Chainlit + Agents SDK

Import the necessary libraries and SDKs for the assistant.

```python
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
```

### Key Notes:
- `chainlit`: Manages the frontend (chat UI).
- `cast`: Helps with static type casting for better editor support.
- `Agent`: Represents the LLM agent.
- `Runner`: Executes the agent.
- `AsyncOpenAI`: A wrapper that supports Gemini via an OpenAI-compatible interface.
- `OpenAIChatCompletionsModel`: Standard model interface.
- `RunConfig`: Configuration holder for how the agent should run.

---

## ⚙️ 3. Session Start — `@cl.on_chat_start`

Define the session start logic.

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

### Key Notes:
- Initializes the assistant with the Gemini API.
- Stores chat history, configuration, and agent in the session.
- Sends a welcome message to the user.

---

## 💬 4. Handling Each Message — `@cl.on_message`

Define how the assistant processes user messages.

```python
@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
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

### Key Notes:
- Sends a placeholder message ("Thinking...") while waiting for the LLM response.
- Retrieves the agent, configuration, and chat history from the session.
- Updates the chat history and sends the assistant's response.
- Logs user and assistant messages for debugging.
- Handles errors gracefully by displaying them to the user.

---

## 🧠 Key Concepts You Must Remember to Master This

| Concept                  | Why It's Important                                                                 |
|--------------------------|-------------------------------------------------------------------------------------|
| Session state (`cl.user_session`) | Keeps track of config, agent, and history per user.                              |
| Agent object             | Represents the LLM and its instructions.                                           |
| `Runner.run_sync(...)`   | Executes the agent using all prior history.                                        |
| History handling         | Provides memory to the assistant — LLMs are stateless without it.                  |
| Async message updates    | Makes the chat responsive — shows "Thinking..." then updates with the actual reply. |

--- 

Follow these steps to set up and use the Panaversity AI Assistant effectively. Happy coding!
