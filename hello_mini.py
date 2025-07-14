from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

resp = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "mini"),   # ← ここを model=
    messages=[{"role": "user", "content": "こんにちは!"}],
    temperature=0.7
)
print(resp.choices[0].message.content)