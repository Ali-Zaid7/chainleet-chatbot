from agent import Agent,Runner,AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = config("GEMINI_API_KEY", default=os.getenv("GEMINI_API_KEY"))
client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

weather_agent = Agent(
    name="Weather Assistant",
    instructions="Provide weather updates and forecasts.",
    model="gemini-2.0-flash",
)

result = Runner.run_sync(
    starting_agent=weather_agent,
    input="What is the weather like today in New York?",
)
print(result.final_result.output)

