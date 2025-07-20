# Global level
import os
import chainlit as cl
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Model provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model config
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", provider=provider)
run_config = RunConfig(model=model, model_provider=provider, tracing_disabled=True)

# Agent setup
agent = Agent(name="Joker", instructions="You are joker", run_config=run_config)

# Chainlit UI handler
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    result = await Runner.run(agent, user_input, run_config=run_config)
    await cl.Message(content=result.output).send()
