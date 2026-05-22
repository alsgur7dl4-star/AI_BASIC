from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

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

# openai 클라이언트 인스턴트 생성
client = OpenAI()

#캐릭터 생성 프롬프트
ARIA_BS_PROMPT = (
"젊은 여성 AI 비서 아리아, 짧은 검은 머리. 뜨듯한 갈색 눈"
"파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,"
"50mm 렌즈, 눈높이, 영화같은 조명, 사실적인 표현")

# GPT-image / 동기 호출 : 응답이 올 떄까찌 기다리기
response = client.images.generate(
  model="gpt-image-2", # # 그림 그릴떄 어떤 "모델"로 요청할지
  prompt=ARIA_BS_PROMPT, # 그림 그릴떄 어떤 "프롬프트"로 요청할지
  size="1024x1024", # 그림"해상도"를 어떻게 요청할지
  quality="low", # 그림"표상도"를 어떻게 요청할지
  n=1, # 그림"몇장" 요청할지
  output_format="png"
)

# 응답 구조 확인 : b64_json 구조 
image_64 = response.data[0].b64_json
print(f"[응답구조] response.data[0].b64_json : {image_64[:60]}...")

# base64 디코딩 후 저장
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
image_bytes = base64.b64decode(image_64)

output_path = output_dir / "aria_v2.png"
output_path.write_bytes(image_bytes)
print(f"[저장 완료] {output_path}")