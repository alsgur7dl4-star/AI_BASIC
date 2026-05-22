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

BASE_PROMPT = (
    " 아리아, 한국인 여성 20대 중반, 은은한 하이라이트가 들어간 짧은 검은 머리. 뜨듯한 갈색 눈"
    "파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소,"
    "사실적인 표현"
)


# 영상 프롬프트 기본 구조
# 이미지 프롬프트는 감상문이 아니다. 촬영 지시서이다.
# prompt = f"{캐릭터 외모}, {샷 사이즈}, {렌즈}, {앵글} , {조명}, {스타일 마무리}

# 기본 프롬프트
APPEARANCE = (
  "젊은 여성 AI 비서 아리아."
  "은백색의 짧은 머리에 파란 눈."
  "하늘색의 미래지향적인 제킷, 온화한 미소"
)

# 6종 샷 사이즈 레퍼런스 카드
# S = ["exterm colose-up", "close-up"]
# 샷 의미 : 카메라와 
SHOT_SIZES = {
  "ECU": ("exteme", "감정 미세 변화, 눈빛 강조"),
  "CU": ("close-up", "얼굴 중심, sns 프로필"),
  "BS": ("bust shot", "표준 포트레이트 - 캐릭터 가드 기준"),
  "MS": ("medium shot", "제스처, 옷차림 포함"),
  "FS": ("full shot", "전신, 의상 카탈로그"),
  "WS": ("wide shot", "환경, 세계관 등 강조"),
}

# 앵글 3종
ANGLES = [
  "eye-level", # 기본 - 친군하고, 자연스러운
  "low angle", # 올려보기 - 위임, 파워, 영웅 등장
  "high angle" # 노려보기 - 귀엽고 , 관찰되는 느낌
  ]

# 조명 3종
LIGHTING_SETUPS = [
  "key light", # 주광 - 밝고 상업적
  "fill light", # 보조광 - 그림자 완화, 자연스러움
  "back light" # 후면광 - 윤곽 강조, 드라마틱
]

# 렌즈
LENSES = [
"24mm wide",
"50mm portrait",
"85mm tight"
]

# 심도
DEPTHS = [
  "shallow depth of field, bokeh background",
  "deep focus, sharp background",
]

prompt = f"{BASE_PROMPT}, {SHOT_SIZES['BS'][0]}, {ANGLES[2] }, {LIGHTING_SETUPS[1]},{LENSES[2]}, {DEPTHS[0]}"

print("gpt-image-1 호출 시작 = 약 5 ~ 15초 소요 예상...")

# DALL-E 3 동기 호출 - 응답이 올 떄까지 기다림
response = client.images.generate(
  model="gpt-image-1.5", # # 그림 그릴떄 어떤 "모델"로 요청할지
  prompt=prompt, # 그림 그릴떄 어떤 "프롬프트"로 요청할지
  size="1024x1024", # 그림"해상도"를 어떻게 요청할지
  quality="low",
  n=1, # 그림"몇장" 요청할지
)

image_b64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_b64)
  
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "aria_v5.png"
output_path.write_bytes(image_bytes)
print(f"[저장완료] {output_path}") 

