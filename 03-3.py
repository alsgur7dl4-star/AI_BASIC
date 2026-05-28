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

scene = {
"scene_kr" : "아리아는 비 오는 오후에 작은 카페 창가에서 낡은 지도를 발견했다.",
"prompt_en" : "Aria is a young woman who is looking at a map in a cafe in the afternoon.",
"shot" : "close-up",
"angle" : "eye-level",
"light" : "soft, diffused light",
}

REQUIRED_FIELDS = {"scene_kr", "prompt_en", "shot", "angle", "light"}

def validate_scene(scene: dict) -> None:
  missing = REQUIRED_FIELDS = set(scene)
  if missing:
    print("없는 필드: ", missing)

# prompt_en 에 시각 정보가 있는지 확인
prompt = scene["prompt_en"].lower()

visual_words = ["shot", "angle", "light"]
if not any(word in prompt for word in visual_words):
  print("prompt_en에 샷, 앵글, 조명 등의 표현이 부족합니다.")

validate_scene(scene)
