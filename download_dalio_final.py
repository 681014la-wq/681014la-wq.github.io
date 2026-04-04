import requests

# 사용자 제공 브릿지워터 공식 이미지 (DOM 분석 기반 직접 경로)
dalio_url = "https://www.bridgewater.com/static/0000017c-5a6b-d3b2-a7fc-5e7f1f6c0000/our-founder-ray-dalio.jpg"
filename = "bg_dalio.jpg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print(f"Downloading official Dalio portrait...")
    response = requests.get(dalio_url, headers=headers, timeout=20)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Success: bg_dalio.jpg saved.")
    else:
        print(f"Failed again (Status {response.status_code}). Trying alternative high-res source...")
        # 위키미디어 원본 (6.7MB) 사용
        alt_url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/Web_Summit_2018_-_Forum_-_Day_2%2C_November_7_HM1_7481_%2844858045925%29.jpg"
        response = requests.get(alt_url, headers=headers, timeout=20)
        if response.status_code == 200:
             with open(filename, 'wb') as f:
                f.write(response.content)
             print("Success: bg_dalio.jpg saved (Alternative source).")
except Exception as e:
    print(f"Error: {e}")
