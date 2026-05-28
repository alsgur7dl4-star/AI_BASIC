import sys

from openai import OpenAI
from pathlib import Path
from agents.sences import extract_scenes
from agents.sences import validate_scenes
from agents.sences import save_scenes
from agents.images import generate_image

def scenes():
    diary_path = Path("diary.md")

    if diary_path.exists():
        diary_text = diary_path.read_text(encoding="utf-8")
        print(f"[diary.md] {len(diary_text)}자 로드 완료")
    else:
        diary_text = (
            "오늘은 비가 내리는 아침, 버스를 기다리며 하늘을 올려다봤다. "
            "작은 카페에 들어가 따뜻한 라떼를 주문했고, 창가 자리에서 낡은 지도를 발견했다. "
            "지도를 펼치자 아직 가보지 못한 도시들의 이름이 보였다. "
            "비가 그치기 시작할 무렵, 나는 여행을 가겠다고 마음을 정했다."
        )
        print(f"[예제일기] {len(diary_text)}자 로드 완료")


    print("[1] 장면 추출 중...")
    scenes = extract_scenes(diary_text)
    print(f"-> {len(scenes)}개 장면 추출 완료")


    print("[2] 장면 검증 중...")
    errors = validate_scenes(scenes)

    if errors:
        print("검증 오류 발생:")
        for err in errors:
            print("-", err)
    else:
        print("-> 검증 완료")

    print("[3] scene_extracted.json 저장 중...")
    save_scenes(scenes, "scene_extracted.json")
    print("-> 저장 완료")
    return scenes["scenes"]

def images(scene, backend):
    generate_image(scene, backend)

if __name__== "__main__":
    # scene = scenes()
    test_diary = (
        "오늘 아침 카페엣 일기를 썻다."
        "점심에는 공원을 걷다가 꽃을 봤다."
        "저녁에는 집에서 요리를 했다."
        "밤에는 창가에서 책을 읽었다."
    )
    scene_s = extract_scenes(test_diary)
    for i, scene in enumerate(scene_s , 1):

        image_path = images(scene, "gpt")
        print(image_path)
    