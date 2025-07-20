# 🧱 1. Environment Setup

```python
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the GEMINI API key from the environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Ensure the API key is defined
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
```

---

# 🧠 2. Importing Chainlit + Agents SDK

```python
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
```

- `chainlit`: Handles UI and sessions.
- `cast`: Helps with type checking.
- `Agent`: Defines the AI personality.
- `Runner`: Runs the agent.
- `AsyncOpenAI`: Gemini-compatible OpenAI wrapper.
- `OpenAIChatCompletionsModel`: Model wrapper.
- `RunConfig`: Controls model + provider.

---

# ⚙️ 3. Session Start — @cl.on_chat_start

```python
@cl.on_chat_start
async def start():
    # Create OpenAI-compatible Gemini client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Wrap Gemini model using OpenAI-style interface
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Configure how the model should be run
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # Initialize session variables
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    # Set up the LLM agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model
    )
    cl.user_session.set("agent", agent)

    # Send welcome message
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()
```

---

# 💬 4. Message Handling — @cl.on_message

```python
@cl.on_message
async def main(message: cl.Message):
    # Show placeholder response
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieve agent and config from session
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Load history and append the new user message
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the agent using history and config
        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        # Extract and send the model's response
        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        # Save updated history for context
        cl.user_session.set("chat_history", result.to_input_list())

        # Debug logging
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        # Show error to user
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
```

---

# 🧠 Key Concepts to Master

| Concept                         | Why It's Important                                                 |
|---------------------------------|---------------------------------------------------------------------|
| `cl.user_session`               | Keeps track of config, agent, history per user                     |
| `Agent` object                  | Your brain — the LLM and its instructions                          |
| `Runner.run_sync(...)`          | Actually runs the agent using all the history                      |
| History handling                | Gives memory to the assistant — LLMs are stateless without it      |
| Async message updates           | Makes the chat responsive — show "Thinking..." then update         |
