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

prompt = "Aria sitting by the cafe window on a rainy afternoon examining an ald map."
response = client.images.generate(
  model="gpt-image-2", # # 그림 그릴떄 어떤 "모델"로 요청할지
  prompt=prompt, # 그림 그릴떄 어떤 "프롬프트"로 요청할지
  size="1024x1024", # 그림"해상도"를 어떻게 요청할지
  quality="auto", # 그림"표상도"를 어떻게 요청할지
  n=1, # 그림"몇장" 요청할지
  output_format="png"
)

print(response)

image_b64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_b64)
  
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "day3-5.png"
output_path.write_bytes(image_bytes)
print(f"[저장완료] {output_path}") 

