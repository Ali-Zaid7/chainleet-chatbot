## Run Google Gemini with OPENAI-Agent SDK
import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,Runner
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v)1beta/openai/"),
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Gemini Agent", instructions="You are a helpful assistant." , model=model)
result = Runner.run_sync(agent, "Who is Mohammad", run_config=config)
print(result.final_output)