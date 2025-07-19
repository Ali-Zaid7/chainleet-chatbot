import asyncio
from agents import Agent , Runner ,OpenAIChatCompletionsModel,AsyncOpenAI ,set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY =os.getenv("GEMINI_API_KEY")
client=AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
set_tracing_disabled(True)
async def main():
    agent = Agent(
        name="Agenta",
        instructions="Psycho and mental human .",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    )
    query = input("Enter your query: ")
    # Using the synchronous run method
    result = Runner.run_streamed(agent, input=query)
    async for event in result.stream_events():
        #stream_events() will yield events as they occur
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())