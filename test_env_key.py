from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

open_api_key: str | None = os.getenv("OPENAI_API_KEY")

def mask_key(key):
  return key[:5]

if open_api_key is None:
  print(".env 로드 오류")
else:
  print(f"{mask_key(open_api_key)}")