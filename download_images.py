"""
JooN's Sushi 메뉴 이미지 다운로더 (통합)
기본 모드: requests 기반 다운로드
--high-res: 고화질 (1200px) + 브라우저 세션 모방
--force: 이미 존재하는 이미지도 재다운로드
"""
import json
import os
import shutil
import sys
import requests
import time

BASE_DIR = r'c:\joon_toy\joon_menu'
JSON_PATH = os.path.join(BASE_DIR, 'menu.json')
IMAGE_DIR = os.path.join(BASE_DIR, 'images')

HEADERS_BASIC = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://joonssushimurrieta.com/menu'
}

HEADERS_HIGHRES = {
    **HEADERS_BASIC,
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# 브라우저에서 직접 복사한 쿠키 (만료 시 갱신 필요)
# Chrome DevTools > Application > Cookies 에서 복사
COOKIES_HIGHRES = {
    '__cf_bm': 'REPLACE_WITH_FRESH_COOKIE',
    'owner-stable-id': 'aecbd047-d354-4c0f-bb4a-88d9ffb284ec',
}


def clean_filename(name):
    return "".join([c if c.isalnum() or c in ' ._-' else '_' for c in name])


def backup_json():
    if os.path.exists(JSON_PATH):
        bak = JSON_PATH + '.bak'
        shutil.copy2(JSON_PATH, bak)
        print(f"백업 생성: {bak}")


def download_images(high_res=False, force=False):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    backup_json()

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        menu_data = json.load(f)

    session = requests.Session()
    if high_res:
        session.headers.update(HEADERS_HIGHRES)
        for name, value in COOKIES_HIGHRES.items():
            session.cookies.set(name, value, domain='joonssushimurrieta.com')
        print("고화질 모드 (1200px, 브라우저 세션)")
    else:
        session.headers.update(HEADERS_BASIC)
        print("기본 모드")

    total = sum(1 for item in menu_data if item.get('original_url'))
    downloaded = 0
    skipped = 0

    for i, item in enumerate(menu_data):
        url = item.get('original_url')
        if not url:
            continue

        file_name = f"{clean_filename(item['name']).replace(' ', '_')}.jpg"
        file_path = os.path.join(IMAGE_DIR, file_name)

        if os.path.exists(file_path) and not force:
            skipped += 1
            continue

        if high_res and '?w=' in url:
            url = f"{url.split('?')[0]}?w=1200&fit=max"

        print(f"[{downloaded+skipped+1}/{total}] {item['name']}...", end=" ")

        try:
            response = session.get(url, timeout=20)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                item['local_path'] = os.path.join('images', file_name)
                downloaded += 1
                print("OK")
            elif response.status_code == 403 and high_res:
                print(f"403 Forbidden - 쿠키 만료 가능성. Chrome DevTools에서 쿠키 갱신 필요")
            else:
                print(f"실패 ({response.status_code})")

            time.sleep(1 if high_res else 0.5)

        except Exception as e:
            print(f"에러: {e}")

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=2)

    print(f"\n완료: 다운로드 {downloaded}, 스킵 {skipped}, 총 {total}")


if __name__ == "__main__":
    high_res = '--high-res' in sys.argv
    force = '--force' in sys.argv
    download_images(high_res=high_res, force=force)
