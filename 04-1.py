import fal_client
from dotenv import load_dotenv

load_dotenv()

# 동기방식 호출

result = fal_client.subscribe(
  "fal-ai/kling-video/v2/master/image-to-video",
  arguments={
    "prompt": "static shot, gentle smile, subtle breathing, cinematic lighting",
    "image_url": "http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg",
    "duration": "5"
  }
)

print(result["video"]["url"])