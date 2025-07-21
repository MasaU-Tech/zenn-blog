import os, sys, openai
from dotenv import load_dotenv; load_dotenv()

client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)
DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")

dish = sys.argv[1] if len(sys.argv) == 2 else "天ぷら"

resp = client.chat.completions.create(
    model=DEPLOY,
   messages=[{"role":"user","content":f"{dish} の材料を教えて"}],
    temperature=0.7,    # ゆらぎを持たせる
)
print(resp.choices[0].message.content)