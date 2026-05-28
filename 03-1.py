from pathlib import Path
from dotenv import load_dotenv #.env 파일 로드
from openai import OpenAI # llm 호출 라이브러리
import os
import base64
import json
import fal_client
import requests

load_dotenv()
client = OpenAI() # .fia_client()

# 기본 호출 방법
response = client.chat.completions.create(
  model ="gpt-4o-mini",
  messages=[
    {"role" : "system", "content" : "자세하고 친절하게 답하세요"},
    {"role" : "user", "content" : "정면 추출이 무엇인지 한 문장으로 설명하세요"}
  ] 
)

print(response.choices[0].messages.content)