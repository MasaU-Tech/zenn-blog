# sessions/s10/image_gen.py
"""
Azure DALL·E 3 で画像を 1 枚生成し images/s10-generated.png に保存。
ターゲット URI 例:
https://eastus.api.cognitive.microsoft.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01
"""

import os, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- 環境変数／固定値 --------------------------------------------
API_KEY      = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT_ROOT = "https://eastus.api.cognitive.microsoft.com"  # リソースごとに変更
DEPLOYMENT   = "dall-e-3"                                    # デプロイ名
API_VERSION  = "2024-02-01"                                  # Studio 表示と合わせる
OUT_PATH     = Path("images/s10-generated.png")
PROMPT       = "浮世絵風の富士山と桜を描いた壁紙 (16:9)"
# -----------------------------------------------------------------

url = (
    f"{ENDPOINT_ROOT}/openai/deployments/{DEPLOYMENT}/images/generations"
    f"?api-version={API_VERSION}"
)

headers = {"api-key": API_KEY, "Content-Type": "application/json"}
payload = {
    "prompt": PROMPT,
    "n": 1,
    "size": "1024x1024",          # ★ 有効サイズに修正
    # "quality": "standard",      # 必要なら追加
    # "style": "vivid"
}

print("⏳ 画像生成をリクエスト中 …")
resp = requests.post(url, headers=headers, json=payload)
resp.raise_for_status()

# Azure DALL·E 3 は同期レスポンスで URL を返してくる
img_url = resp.json()["data"][0]["url"]
img_bin = requests.get(img_url).content

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH.write_bytes(img_bin)

print(f"✅ 画像生成完了 → {OUT_PATH}")
