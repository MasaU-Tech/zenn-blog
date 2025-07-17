import os           # 環境変数を扱うためのモジュール
import sys          # コマンドライン引数を扱うためのモジュール
import requests     # HTTPリクエストを送るための外部ライブラリー

#メインの処理を行う関数を定義
def main() -> None:
    # コマンドラインの引数の数が正しくない、または「/」が含まれていない場合は終了
    if len(sys.argv) != 2 or "/" not in sys.argv[1]:
        sys.exit("使い方: python github_api.py <owner>/<repo>")    ## 正しい使い方を表示して終了

    # コマンドラインから受け取った「owner/repo」の形式の文字列を分解
    owner, repo = sys.argv[1].split("/", 1)
    # # GitHub APIのURLを作成（指定されたリポジトリの情報を取得）
    url = f"https://api.github.com/repos/{owner}/{repo}"

    # リクエスト用のヘッダーを準備します（認証トークンがあれば追加）
    headers = {}
    if token := os.getenv("GITHUB_TOKEN"):
        # 環境変数「GITHUB_TOKEN」が設定されていれば、それを使って認証
        headers["Authorization"] = f"token {token}"

    try:
         # GitHub APIにリクエストを送ります（最大10秒待機）
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    # エラーが返ってきた場合は例外を発生させます（例えば存在しないリポジトリなど）
    except requests.HTTPError as e:
        #  # エラー内容を表示して終了
        sys.exit(f"GitHub API エラー: {e}")

    # APIの返り値（JSON形式）からスター数（stargazers_count）を取得
    # 値が見つからない場合は0を返す
    stars = r.json().get("stargazers_count", 0)
    # 結果を表示
    print(f"⭐ {owner}/{repo} → {stars} Stars")

# このファイルが直接実行されたときだけ、main関数を呼び出し
if __name__ == "__main__":
    main()
