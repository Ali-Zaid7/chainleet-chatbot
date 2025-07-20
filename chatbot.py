import os 
import chainlit as cl
from typing import cast #Helps with static type casting for better editor support.
from agents import Agent ,Runner, AsyncOpenAI, OpenAIChatCompletionsModel #AGENT:Represents the LLM agent
#RUNNER:Executes the agent, AsyncOpenAI: A wrapper that supports Gemini via OpenAI-compatible interface.
#OpenAIChatCompletionsModel: Standard model interface.,RunConfig: Configuration holder for how the agent should run.
from agents.run import RunConfig
from dotenv import load_dotenv

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini api key is Missing!")

#⚙️ 3. Session Start — @cl.on_chat_start
@cl.on_chat_start
async def start():
    #Runs once when the user first connects to the chatbot.
    external_client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
#🔗 This uses Gemini API through an OpenAI-compatible wrapper.
    model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client)
#OpenAIChatCompletionsModel wraps Gemini as if it's a ChatGPT-style model.
    config = RunComfig(model=model, model_provider=external_client, tracing_disaabled=True)
#All configuration is grouped here (model, provider, optional tracing).
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
#Stores chat history and config in the session. This data persists across user messages.
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model=model)
    cl.user_session.set("agent", agent)
#Initializes the agent, binds it to the model, and stores it in the session.
    await cl.Message(content="Salam from Panaversity AI Assistant! How can I help you today?")
#First message the assistant sends.
    
##💬 4. Handling Each Message — @cl.on_message
@cl.on_message
async def handle_message(message: cl.Message):
    # Called every time the user sends a message.
    msg = cl.Message(content="Thinking...")
    try:
        await msg.send()
        # This sends a placeholder while we wait for the LLM response.
        agent: Agent = cast(Agent, cl.user_session.get("agent"))
        config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
        # Retrieves the agent and config from session memory.
        history = cl.user_session.get("chat_history") or []
        history.append({"role": "user", "content": message.content})
        # Pulls chat history from the session and adds the new user message.
        result = Runner.run_sync(starting_agent=agent, input=history, run_config=config)
        # Calls the agent synchronously, using all prior history.
        response_content = result.final_output
        msg.content = response_content
        await msg.update()
        # Updates the "Thinking..." message with the actual assistant reply.
        cl.user_session.set("chat_history", result.to_input_list())
        # Updates the "Thinking..." message with the actual assistant reply.
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        # Logging for debug purposes.
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        # In case anything fails, show the error.