from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import os
import base64
import json

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

client = OpenAI()

def json_mode():
  response = client.chat.completions.create(
    model = "gpt-4o-mini",
    response_format={"type" : "json_object"}, # 요청 포켓
    messages=[
        {
        "role" : "system",
        "content" : (
          "당신은 한 줄 문장을 json 객체로 변환하는 도우미입니다."
          "반드시 다음 형식으로만 답하세요."
          '{"title" : "제목 한 줄", "word_count" : "단어수(점수)"}'   
        )
      },
        {
        "role" : "user",
        "content" : (
          "아리아가 도서관에서 책을 읽고 있습니다."
        )
      },
    ]
  )

  result = json.loads(response.choices[0].message.content)

  print(result)
  print(type(result))

def no_json_mode():
  response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {
        "role" : "system",
        "content" : (
          "당신은 한 줄 문장을 json 객체로 변환하는 도우미입니다."
        )
        },
        {
        "role" : "user",
        "content" : ("아리아가 도서관에서 책을 읽고 있습니다.")
        },
    ]
  )

  result = json.loads(response.choices[0].message.content)

  print(result)
  print(type(result))




def response_json():
  response = client.chat.completions.create(
    model = "gpt-4o-mini",
    response_format={"type" : "json_object"}, # 요청 포켓
    messages=[
        {
        "role" : "system",
        "content" : (
          "JSON 형식으로 답하세요."
          '형식: {"name":"이름", {"age"}:"나이"}'   
        )
      },
        {
        "role" : "user",
        "content" : (
          "아리아의 이름과 나이를 알려주세요"
        )
      },
    ]
  )

  result = json.loads(response.choices[0].message.content)

  print(result)
  print(type(result))  

if __name__ == "__main__":
  # json_mode()
  # no_json_mode()
  response_json()