import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()
LITELLM_URL = os.getenv("LITELLM_URL")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")

model = OpenAIChatModel(
    model_name="ollama/mistral:7b",
    # model_name="gpt-4",
    provider=OpenAIProvider(
        base_url=LITELLM_URL,
        api_key=LITELLM_API_KEY,
    ),
)

agent = Agent(
    model=model,
)

response = agent.run_sync("What is the capital of France?")
print(response.output)
