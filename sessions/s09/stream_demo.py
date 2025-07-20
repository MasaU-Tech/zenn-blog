"""gpt-4o mini からストリーム応答を受け取りながら表示する"""

import os, sys
from dotenv import load_dotenv
import openai
# os：環境変数（設定ファイルなど）を読み取るために使う
# sys：コマンドライン引数（入力）を受け取るために使う
# load_dotenv：.envファイルという設定ファイルからAPIキーなどを読み込み
# openai：Azure OpenAI APIを使うためのライブラリ

load_dotenv()

client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)

DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # 例: mini

# .envファイルに書いてある秘密情報（APIキー、エンドポイント、モデルの名前）を取得
# client はAzure OpenAIのチャット機能を使うための準備
# DEPLOY は使うチャットモデルの「名前」（Azureで設定されているもの）

def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("使い方: python stream_demo.py <質問文>")
        # コマンドラインで質問が入力されなかったら終了
        # 使い方の例：python stream_demo.py 明日の天気は？
    user = " ".join(sys.argv[1:])
        #質問の部分（コマンドラインで入力した文字列）を user に代入

    stream = client.chat.completions.create(
        model=DEPLOY,
        messages=[
            {"role": "system", "content": "あなたは丁寧な日本語で答えるアシスタントです。"},
            {"role": "user",   "content": user},
        ],
        stream=True,            # ★ ストリーミング ON
        max_tokens=512,
    )
# ChatGPTに質問を送信
# system メッセージで「丁寧な日本語で答えてください」と指示
# stream=True により、回答が少しずつ届く（リアルタイム表示用）

    ...
    print("🤖:", end=" ", flush=True)
    for chunk in stream:
        if not chunk.choices:          # ★ 追加: 空チャンクを無視
            continue
        choice = chunk.choices[0]
        delta = getattr(choice, "delta", None)
        if delta and delta.content:
            print(delta.content, end="", flush=True)
    print()  # 改行
    # チャットの返答を少しずつ表示
    # たとえば長文なら、1文字ずつ or 1単語ずつ画面に出てくる感じ
    # flush=True は「すぐに表示する」ための指定

if __name__ == "__main__":
    main()
# このスクリプトが直接実行されたときだけ main() を動かす