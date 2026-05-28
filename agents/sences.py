import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

SYSTEM_PROMPT = """
당신은 일기 텍스트를 분석하여 그림일기용 4장면을 추출하는 어시스턴트입니다.
출력은 반드시 JSON 객체여야 합니다. 다음 스키마를 따릅니다.
{
  "scenes": [
    {
      "scene_id": int,
      "scene_kr": "한국어 1줄 장면 설명",
      "prompt_en": "영문 이미지 프롬프트 1줄"
    }
  ]
}
반드시 4개 장면을 추출합니다.
prompt_en은 반드시 영어로 작성하고 wide shot/medium shot/close-up, eye-level/low/high angle, soft/rim/backlit lighting,
watercolor diary illustration 스타일을 포함합니다.
scene_id는 1부터 시작하는 정수입니다.
"""


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 .env에 있는지 확인합니다.")

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1500,
    )

    content = response.choices[0].message.content
    data = json.loads(content)

    scenes = data.get("scenes", [])

    return scenes


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면이고 필수 필드를 충족하는지 검증합니다."""
    errors: list[str] = []

    if len(scenes) != 4:
        errors.append(f"장면 수 오류: {len(scenes)}개 (총 4개 필요)")

    required_fields = {"scene_id", "scene_kr", "prompt_en"}

    for i, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            errors.append(f"장면 {i} 타입 오류: dict가 아님")
            continue

        missing = required_fields - set(scene.keys())

        if missing:
            errors.append(f"장면 {i} 필드 누락: {missing}")

    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장합니다."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w", encoding="utf-8") as f:
        json.dump({"scenes": scenes}, f, ensure_ascii=False, indent=2)