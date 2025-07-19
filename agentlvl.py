import asyncio
import os
from dotenv import load_dotenv
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    set_tracing_disabled,
    set_default_openai_api,
    set_default_openai_client,
    AsyncOpenAI
)

BASE_URL = os.getenv("BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDmnI3YpwS2s4tIHP1jyBZp4iHxd0nEEng"
MODEL_NAME = os.getenv("MODEL_NAME") or "gemini-2.0-flash"

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("BASE_URL, API_KEY, and MODEL_NAME must be set in the environment variables or userdata dictionary.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f" The weather in {city} is sunny with a high of 25°C."

async def main():
    agent = Agent(
        name="Assistant", instructions="You are wether bot.", model=MODEL_NAME, tools=[get_weather]
    )
    prompt = input("City:")
    result = await Runner.run(agent, f"What is the weather in {prompt}")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())