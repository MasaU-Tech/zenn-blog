import os, sys
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)

DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")
SYSTEM = "You are a friendly Japanese assistant."

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("使い方: python openai_hello.py <ユーザー発話>")

    resp = client.chat.completions.create(
        model=DEPLOY,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": sys.argv[1]},
        ],
        max_tokens=64,
        temperature=0.7,
    )
    print("🤖:", resp.choices[0].message.content.strip())

if __name__ == "__main__":
    main()
