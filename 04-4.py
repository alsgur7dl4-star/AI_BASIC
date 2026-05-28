from dotenv import load_dotenv
import os
from openai import OpenAI
import fal_client
import requests

load_dotenv()
client = OpenAI()

aria = {
    "name" : "Aria",
    "role": "젊은 남성 AI PT, 운동 도우미",
    "apperance":"짧은 검은 머리, 갈색 눈, 친근한 미소",
    "outfit":"은은한 파란색 포인트가 들어간 흰색 츄리닝 복장",
    "mood": "친근하고, 전문적이고, 상냥함"
} 

def agent_designer(character : dict) -> str:
    """디자이너: 캐릭터 dict -> 시각화 프롬프트 문자열로 반환"""
    # return f"{character['apperance']}, cinematic lighting, photorealistic"
    appearance = (
        f"{character['role']}, {character['apperance']}, "
        f"{character['outfit']}, {character['mood']}, "
    )
    # print(appearance)
    shot = "bust shot, 50mm lens, eye-level, soft key light, cinematic lighting, photorealisic"
    return f"{appearance, shot}"
    
def agent_photorgrapher(prompt: str) -> str:
    """사진작가: prompt -> 이미지 생성 -> url"""
    # return f"https://example.com/images/{prompt[:10].replace(' ', '_')}.png"
    r = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )
    return r.data[0].b64_json


def agent_video_director(image_b64:str, name:str) -> str:
    """영상감독: 이미지 url -> 영상 url"""
    # return f"https://example.com/videos/{name}_intro.mp4"
    camera_work = (
        f"static shot, {name} gentle smile, eye blink, "
        "slight head turn, cinematic lighting"
    )
    # 동기
    r = fal_client.subscribe(
        "fal-ai/kling-video/v2/master/image-to-video",
        arguments={
            "prompt":camera_work,
            "image_url" : f"data:image/png;base64,{image_b64}",
            "duration": "5",
        }
    )
    return r["video"]["url"]

def character_piplin(character:dict)-> dict:
    """파이프라인: 3개의 에이전트를 순서대로 전부 호출"""
    print(f"캐릭터 카드 제작 시작 : {character['name']}")
    prompt = agent_designer(character)
    image_url = agent_photorgrapher(prompt)
    video_url = agent_video_director(image_url,character["name"])
    return {
        "name" : character['name'],
        "image_url":image_url,
        "video_url":video_url
    }

# 실행
# aria = {"name":"Aria", "apperance":"short black hair, warm brom eyes, friendly smile"}
card = character_piplin(aria)
print(f"{aria['name']} 캐릭터 카드 완성")
print(f"영상 url: {card['video_url']}")