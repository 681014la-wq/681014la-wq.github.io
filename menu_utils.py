"""
JooN's Sushi 메뉴 - 공통 유틸리티
build_ppt.py, build_html.py, build_tv.py 에서 공유
"""
import os
import re
import base64

IMAGE_DIR = "images"


def find_local_image(name):
    """메뉴 이름으로 로컬 이미지 파일 경로를 찾는다."""
    if not os.path.exists(IMAGE_DIR):
        return None
    safe = name.strip()
    for pat in [f"{safe}.jpg", f"{safe} (1).jpg"]:
        p = os.path.join(IMAGE_DIR, pat)
        if os.path.exists(p):
            return p
    for f in os.listdir(IMAGE_DIR):
        base = re.sub(r'\s*\(\d+\)$', '', os.path.splitext(f)[0].strip())
        if base.lower() == safe.lower():
            return os.path.join(IMAGE_DIR, f)
    return None


def img_to_base64(path):
    """이미지 파일을 base64 data URI로 변환한다."""
    if not path or not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"


def truncate_text(text, max_len=80):
    """텍스트를 단어 단위로 잘라낸다."""
    if not text or len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(' ', 1)[0]
    return truncated + "..."
