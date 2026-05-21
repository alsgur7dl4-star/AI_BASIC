import os
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import base64


# API KEY 로드 되었는지 확인
load_dotenv()
api_key: str | None = os.getenv("OPENAI_API_KEY")
# print(api_key)

# openai 클라이언트 생성(키 자동 탐지)
client = OpenAI()

#캐릭터 생성 프롬프트
ARIA_BS_PROMPT = (
"젊은 여성 AI 비서 아리아, 짧은 검은 머리. 뜨듯한 갈색 눈"
"파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,"
"50mm 렌즈, 눈높이, 영화같은 조명, 사실적인 표현")

print("DALL-E 3 호출 시작 = 약 5 ~ 15초 소요 예상...")

# DALL-E 3 동기 호출 - 응답이 올 떄까지 기다림
response = client.images.generate(
  model="gpt-image-1", # # 그림 그릴떄 어떤 "모델"로 요청할지
  prompt=ARIA_BS_PROMPT, # 그림 그릴떄 어떤 "프롬프트"로 요청할지 
  size="1024x1024", # 그림"해상도"를 어떻게 요청할지
  n=1, # 그림"몇장" 요청할지
)

if not response.data:
  raise Exception("이미지 응답 데이터가 비어 있습니다.")

image_data = response.data[0]

# URL 에서 PNG 다운로드 후 저장
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

image_bytes = base64.b64decode(image_data.b64_json)

# PNG 파일 저장
output_path = output_dir / "aria_v1.png"
output_path.write_bytes(image_bytes)

print(f"[저장완료] {output_path}") 
