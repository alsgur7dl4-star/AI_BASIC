from pathlib import Path
from dotenv import load_dotenv  # .env 파일 로드
from openai import OpenAI  # llm 호출 라이브러리
import os
import base64
import json
import fal_client
import requests

load_dotenv()
client = OpenAI()

REQUIRED_FIELDS = {"scene_kr", "prompt_en", "shot", "angle", "light"}

SCENE_SCHEMA_HINT = """
너는 그림일기 장면 추출 담당자입니다.
반드시 JSON 객체로만 답합니다.
최상위 키는 scenes입니다.
각 장면은 scene_kr, prompt_en, shot, angle, light을 포함합니다.
prompt_en은 영어로 쓰고, 샷, 앵글, 조명 표현을 포함합니다.
장면은 최대 3개입니다.
"""

def validate_scene(scene: dict) -> None:
    missing = REQUIRED_FIELDS - set(scene.keys())

    if missing:
        print("없는 필드:", missing)

def extract_scenes(text: str) -> list[dict]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SCENE_SCHEMA_HINT},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    scenes = data.get("scenes", [])[:3]

    for scene in scenes:
        validate_scene(scene)

    return scenes

if __name__ == "__main__":
    diary = "아리아는 비 오는 오후 카페 창가에서 낡은 지도를 발견했다."

    for item in extract_scenes(diary):
        print(item["scene_kr"])
        print(item["prompt_en"])