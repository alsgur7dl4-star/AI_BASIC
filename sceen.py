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

# 기본 프롬프트
APPEARANCE = (
  "젊은 여성 AI 비서 아리아."
  "은백색의 짧은 머리에 파란 눈."
  "하늘색의 미래지향적인 제킷, 온화한 미소"
)

# 프롬프ㅡ 조합 함수
def build_prompt(scene: dict) -> str:
    """"JSON 장면 필드 딕셔너리에서 llm을 프롬프트 조합"""

    parts = [
        APPEARANCE,
        f"{scene['shot']} shot", # 카메라 거리
        scene['angle'],          # 앵글
        scene['light'],          # 조명
        f"{scene['lens']} lens", # 렌즈
        scene["composition"]     # 구도

    ]
    return ", ".join(parts)

# 장면 설정 json
sample_scene = {
    "scene_id" : 1,
    "scene_kr" : "Aria의 집중된 표정 클로즈업",
    "shot" : "CU",
    "angle" : "eye-level",
    "light" : "key light",
    "lens" : "85mm tight",
    "composition" : "contrast"
  }

prompt = build_prompt(sample_scene)
print(prompt)