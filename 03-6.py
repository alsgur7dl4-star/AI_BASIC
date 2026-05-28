from pathlib import Path
from dotenv import load_dotenv  # .env 파일 로드
from openai import OpenAI  # llm 호출 라이브러리
import os
import base64
import json
import fal_client
import requests



def get_client() -> OpenAI:
  load_dotenv()
  api_key = os.getenv("OPENAI_API_KEY")
  if not api_key:
    raise ValueError("OPENAI_API_KEY가 .ENV에 없습니다.")  

# client = get_client()

def get_scene_prompt() -> str:
  # extract_scens 결과에서 prompt_en을 꺼냅니다.
  scenes = {
    "scene_kr" : "아리아가 비 오는 오후 카페 창가에서 낡은 지도를 바라보고 있는 장면입니다."
    "prompt_en" : "Aria sitting by the cafe window on a rainy afternoon examining an ald map."
}  

def penerate_one_image(client: OpenAI, prompt: str):
  return client.images.generate(
  model="gpt-image-2", # # 그림 그릴떄 어떤 "모델"로 요청할지
  prompt=prompt, # 그림 그릴떄 어떤 "프롬프트"로 요청할지
  size="1024x1024", # 그림"해상도"를 어떻게 요청할지
  quality="auto", # 그림"표상도"를 어떻게 요청할지
  n=1, # 그림"몇장" 요청할지
  output_format="png"
  )
