import os, openai, sys
from dotenv import load_dotenv; load_dotenv()
# os: 環境変数を取得するため。
# sys: コマンドライン引数（問題文）を受け取るため。
# openai: Azure OpenAI API を使うため。
# dotenv: .env ファイルからAPIキーやエンドポイントを読み込む。

client  = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)
DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")
# .env ファイルに書かれた以下の情報を取得：
#     AZURE_OPENAI_API_KEY（APIキー）
#     AZURE_OPENAI_ENDPOINT（エンドポイントURL）
#     AZURE_OPENAI_DEPLOYMENT（デプロイ名)


question = sys.argv[1] if len(sys.argv) == 2 else "500円のりんごを3個と200円のバナナを2本買うと合計はいくら？"
# 実行時に引数を指定すればそれを問題文として使用
# 指定されない場合はデフォルトの文章問題を使う

prompt = (
    "次の算数問題を Chain-of-Thought で解いてください。"
    "まず『考え』を段階的に書き、最後に『答え: <数字>円』と出力してください。\n"
    f"問題: {question}"
)
# 「最後に『答え: ○○円』と出力してね」と形式を明示
# このような形式を明示することで、人間が理解しやすく、かつ機械でも処理しやすい回答を期待


resp = client.chat.completions.create(
    model=DEPLOY,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
)
# messages: ユーザーからのメッセージとして prompt を送信。
# temperature=0.2: 出力のバラつきを抑えて、より論理的で安定した回答を出させるための設定。

print(resp.choices[0].message.content)
# ChatGPT からの回答を表示
# Chain-of-Thought に従って、途中の考え→最後に答えという構成で出力