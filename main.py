import sys
import importlib



def main():
    print("Hello from ai-basic!")
     # import 이름 기준 리스트 (콤마로 분리된 진짜 리스트)
    packages = [
        "dotenv",
        "openai",
        "fal_client",
        "replicate",
        "transformers",
        "diffusers",
        "PIL",
        "requests",
    ]

    for pkg in packages:
        try:
            mod = importlib.import_module(pkg)
            ver = getattr(mod, "__version__", "버전 정보 없음")
            print(f"{pkg}: {ver}")
        except Exception as e:
            print(f"{pkg}: 임포트 실패 ({e})")



if __name__ == "__main__":
    main()
