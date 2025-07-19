import asyncio
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI
from agents.run import RunConfig
import os
from dotenv import load_dotenv
# 
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client)
config=RunConfig(model=model, model_provider=external_client, tracing_disabled=True)
async def main():
    agent= Agent(name="Async Agent", instructions="You are a helpful assistant.")
    result = await Runner.run(agent, "Who is Abraham", run_config=config)
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.
if __name__ == "__main__":
    asyncio.run(main())

#Agent level configuration
#agent = Agent(name="Async Agent", instructions="You are a helpful assistant.", model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client))