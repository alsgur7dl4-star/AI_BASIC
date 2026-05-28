import fal_client
from dotenv import load_dotenv

load_dotenv()

model_id = "fal-ai/kling-video/v2/master/image-to-video"

# 비동기 방식 호출

result = fal_client.submit(
  model_id,
  arguments={
    "prompt": "static shot, gentle smile, subtle breathing, cinematic lighting",
    "image_url": "http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg",
    "duration": "5"
  }
) 

# print(result.request_id)
request_id = result.request_id
print(f"[1단계] 제출완료 : {request_id}")

while True:
  s = fal_client.status(model_id, request_id)
  if s.get("status") == "COMPLETED": break
  print("진행중...", s.get("status"))
  time.sleep(5)

result = fal_client.result(model_id, request_id)
print(result["video"]["url"])