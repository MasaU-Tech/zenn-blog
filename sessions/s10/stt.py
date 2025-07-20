"""
Whisper translations (音声→英訳) : 別リージョン・別 API Key に対応
"""

import os, sys, json, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---------- Whisper 用変数 ----------
WH_API_KEY   = os.getenv("AZURE_WHISPER_API_KEY")
WH_ENDPOINT  = os.getenv("AZURE_WHISPER_ENDPOINT").rstrip("/")
WH_DEPLOY    = os.getenv("AZURE_WHISPER_DEPLOYMENT", "whisper")
API_VER      = "2024-06-01"
# ------------------------------------

if not WH_API_KEY or not WH_ENDPOINT:
    sys.exit("❌ .env に AZURE_WHISPER_API_KEY / AZURE_WHISPER_ENDPOINT がありません")

if len(sys.argv) != 2 or not Path(sys.argv[1]).exists():
    sys.exit("使い方: python stt.py <audio file>")

file_path = Path(sys.argv[1])
mime = "audio/wav" if file_path.suffix.lower() == ".wav" else "audio/mpeg"

url = f"{WH_ENDPOINT}/openai/deployments/{WH_DEPLOY}/audio/translations?api-version={API_VER}"
headers = {"api-key": WH_API_KEY}

with file_path.open("rb") as f:
    files = {
        "file": (file_path.name, f, mime),
        # Whisper は response_format を省略すると JSON を返す
        # "response_format": (None, "text"),
    }
    print("⏳ Whisper にアップロード …")
    resp = requests.post(url, headers=headers, files=files)

resp.raise_for_status()

# --- JSON or text どちらでも対応 ---
if resp.headers.get("Content-Type", "").startswith("application/json"):
    text = resp.json()["text"].strip()
else:
    text = resp.text.strip()
# -------------------------------------

Path("transcript.txt").write_text(text, encoding="utf-8")
print("✅ transcript.txt 作成\n------\n" + text + "\n------")