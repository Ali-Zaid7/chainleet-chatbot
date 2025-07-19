import asyncio
from agents import Agent , Runner ,OpenAIChatCompletionsModel,AsyncOpenAI ,set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY =os.getenv("GEMINI_API_KEY")
client=AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
set_tracing_disabled(True)
agent = Agent(name="Agenta", instructions="An agent that can run tasks and manage workflows.",
              model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client))
query = "Hello How are u?"
result = Runner.run_sync(
    agent,
    query,
)
print(result.final_output)