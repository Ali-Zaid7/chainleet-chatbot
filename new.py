import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,Runner,enable_verbose_stdout_logging
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
enable_verbose_stdout_logging()

class ChatContext1(BaseModel):
    name:str
    role:str
    last_message:str

agent = Agent(name=None, instructions=None,
              model="gemini-2.0-flash",
              output_type=ChatContext1)

result = Runner.run_sync(agent, "Whaat is recursion in programming?")
print(result.final_output)
set_tracing_disabled(True)