from dotenv import load_dotenv
from openai import OpenAI
import os

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 읽기
api_key: str | None = os.getenv("OPENAI_API_KEY")
# OpenAI Client 생성
client = OpenAI(api_key=api_key)
if api_key is None:
    print(".env 로드 오류: OPENAI_API_KEY가 없습니다.")
else:
    print(f"API 키 로드 성공: {api_key[:5]}...")



# .gitignore에 .env 등록 확인
gitignore_path = ".gitignore"

try:
    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()

        if ".env" in content:
            print(".gitignore에 .env 등록 확인")
        else:
            print(".gitignore에 .env 누락 - 즉시 추가 필요!!")

except FileNotFoundError:
    print(".gitignore 파일 없음")