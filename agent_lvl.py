import asyncio 
import os
from agents import Agent,OpenAIChatCompletionsModel,Runner, function_tool, set_tracing_disabled, AsyncOpenAI
from dotenv import load_dotenv

userdata={"GEMINI_API_KEY": "AIzaSyDmnI3YpwS2s4tIHP1jyBZp4iHxd0nEEng"}

load_dotenv()
BASE_URL = os.getenv("BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY") or userdata.get("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME") or "gemini-2.0-flash"

# print(BASE_URL, API_KEY , MODEL_NAME)

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("BASE_URL, API_KEY, and MODEL_NAME must be set in the environment variables or userdata dictionary.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
    )

    result = await Runner.run(agent, "What is the meaning of life?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())