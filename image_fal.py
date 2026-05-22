from pathlib import Path
from dotenv import load_dotenv
import os
import fal_client
import urllib.request

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 읽기
api_key: str | None = os.getenv("FAL_KEY")

if api_key is None:
    print(".env 로드 오류: FAL_KEY가 없습니다.")
else:
    print(f"API 키 로드 성공: {api_key[:6]}...")

# 캐릭터 생성 프롬프트
ARIA_BS_PROMPT = (
    "젊은 여성 AI 비서 아리아, 짧은 검은 머리, 따뜻한 갈색 눈, "
    "파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷, "
    "50mm 렌즈, 눈높이, 영화같은 조명, 사실적인 표현"
)

print("fal.ai FLUX-schnell 호출 시작 = 약 5 ~ 15초 소요 예상")

# subscribe: 동기 호출 — 큐 등록 → 완료 대기 → 결과 반환 (결과 올 때까지 블로킹)
result = fal_client.subscribe(
    "fal-ai/flux/schnell",
    arguments={
        "prompt": ARIA_BS_PROMPT,
        "image_size": "landscape_4_3",   # square_hd, square, portrait_4_3 등
        "num_inference_steps": 4,         # schnell은 4스텝이면 충분
        "num_images": 1,
    },
)

# 응답 구조 확인
fal_image_url = result["images"][0]["url"]
print(f"[응답 구조] result['images'][0]['url'] = {fal_image_url}")
print("[비용 참고] flux-schnell 모델 사용")

# URL에서 이미지 다운로드 후 저장
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "fal_image_v1.png"

try:
    urllib.request.urlretrieve(fal_image_url, output_path)
    print(f"[저장 완료] {output_path}")
except Exception as e:
    print(f"[저장 실패] {e}")