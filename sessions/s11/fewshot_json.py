import os, json, openai, sys
from dotenv import load_dotenv; load_dotenv()

client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)
DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")

few_shots = [
    # ★ few-shot 例①
    {
        "role": "user",
        "content": "寿司の材料を JSON で出力して",
    },
    {
        "role": "assistant",
        "content": json.dumps({"dish": "寿司", "ingredients": ["米", "酢", "わさび"]}, ensure_ascii=False),
    },
    # ★ few-shot 例②
    {
        "role": "user",
        "content": "味噌汁の材料を JSON で出力して",
    },
    {
        "role": "assistant",
        "content": json.dumps({"dish": "味噌汁", "ingredients": ["味噌", "豆腐", "わかめ"]}, ensure_ascii=False),
    },
]
system_prompt = "必ず **JSON オブジェクトのみ** を返し、前後に説明や ``` は付けない。"

dish = sys.argv[1] if len(sys.argv) == 2 else "天ぷら"
resp = client.chat.completions.create(
    model=DEPLOY,
    messages=[
        {"role": "system", "content": "必ず valid JSON だけを返して"},
        *few_shots,
        {"role": "user", "content": f"{dish} の材料を JSON で出力して"},
    ],
    temperature=0.0,  # 例外を減らす
)
print(resp.choices[0].message.content)
