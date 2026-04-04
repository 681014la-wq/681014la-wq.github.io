"""
JooN's Sushi 메뉴 HTML 생성 - 프리미엄 럭셔리 디자인
"""
import json
import os
from menu_utils import find_local_image, img_to_base64

MENU_JSON = "menu.json"
IMAGE_DIR = "images"
OUTPUT_HTML = "JooNs_Sushi_Menu.html"


def load_menu():
    with open(MENU_JSON, "r", encoding="utf-8") as f:
        menu = json.load(f)
    result = []
    for item in menu:
        local = find_local_image(item["name"])
        if local:
            item["local_image"] = local
            item["img_b64"] = img_to_base64(local)
            result.append(item)
    print(f"전체: {len(menu)}개 → 이미지: {len(result)}개")
    return result


def generate_html(menu):
    # 카테고리별 정리
    cats = {}
    for item in menu:
        c = item["category"]
        if c not in cats:
            cats[c] = []
        cats[c].append(item)

    # 카테고리 네비게이션
    nav_html = ""
    for cat in cats:
        cat_id = cat.lower().replace(" ", "-").replace("'", "")
        nav_html += f'<a href="#{cat_id}" class="nav-link">{cat}</a>\n'

    # 메뉴 섹션별 HTML
    sections_html = ""
    for cat, items in cats.items():
        cat_id = cat.lower().replace(" ", "-").replace("'", "")
        cards = ""
        for item in items:
            cards += f'''
            <div class="menu-card">
                <div class="card-image-wrap">
                    <img src="{item['img_b64']}" alt="{item['name']}" class="card-image" loading="lazy">
                    <div class="image-shine"></div>
                </div>
                <div class="card-content">
                    <h3 class="item-name">{item['name']}</h3>
                    <div class="item-price">{item['price']}</div>
                    <p class="item-desc">{item.get('description', '')}</p>
                </div>
            </div>'''

        sections_html += f'''
        <section class="menu-section" id="{cat_id}">
            <div class="section-header">
                <div class="section-deco">✦</div>
                <h2 class="section-title">{cat}</h2>
                <div class="section-line"></div>
                <span class="section-count">{len(items)} items</span>
            </div>
            <div class="menu-grid">
                {cards}
            </div>
        </section>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JooN's Sushi Menu</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --gold: #C9A96E;
    --gold-light: #E8D4A8;
    --gold-dark: #8B754A;
    --bg-dark: #0A0A12;
    --bg-card: #111119;
    --bg-card-hover: #1A1A28;
    --white: #F0EEE8;
    --gray: #8A857E;
    --border: #2A2420;
}}

body {{
    background: var(--bg-dark);
    color: var(--white);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* ═══ 배경 장식 ═══ */
body::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 0%, rgba(201,169,110,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(201,169,110,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(10,10,18,1) 0%, rgba(10,10,18,0.95) 100%);
    pointer-events: none;
    z-index: -1;
}}

/* ═══ 표지 ═══ */
.cover {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.cover::before {{
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background:
        conic-gradient(from 0deg at 50% 50%,
            transparent 0deg,
            rgba(201,169,110,0.03) 60deg,
            transparent 120deg,
            rgba(201,169,110,0.02) 180deg,
            transparent 240deg,
            rgba(201,169,110,0.03) 300deg,
            transparent 360deg);
    animation: coverRotate 60s linear infinite;
}}

@keyframes coverRotate {{
    to {{ transform: rotate(360deg); }}
}}

.cover-frame {{
    position: relative;
    z-index: 1;
    border: 1px solid var(--gold-dark);
    padding: 60px 80px;
    background: rgba(10,10,18,0.7);
    backdrop-filter: blur(10px);
}}

.cover-frame::before,
.cover-frame::after {{
    content: '✦';
    position: absolute;
    color: var(--gold);
    font-size: 12px;
}}
.cover-frame::before {{ top: -8px; left: 50%; transform: translateX(-50%); }}
.cover-frame::after {{ bottom: -8px; left: 50%; transform: translateX(-50%); }}

.cover-deco {{
    color: var(--gold-dark);
    font-size: 24px;
    letter-spacing: 12px;
    margin-bottom: 20px;
}}

.cover-title {{
    font-family: 'Playfair Display', serif;
    font-size: 82px;
    font-weight: 700;
    color: var(--gold-light);
    letter-spacing: 4px;
    line-height: 1.1;
    text-shadow: 0 0 60px rgba(201,169,110,0.3);
}}

.cover-subtitle {{
    font-size: 28px;
    font-weight: 300;
    letter-spacing: 16px;
    color: var(--white);
    margin-top: 20px;
    opacity: 0.8;
}}

.cover-line {{
    width: 200px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 30px auto;
}}

.cover-address {{
    font-size: 14px;
    color: var(--gray);
    font-weight: 300;
    letter-spacing: 2px;
}}

.cover-url {{
    font-size: 13px;
    color: var(--gold-dark);
    margin-top: 8px;
    letter-spacing: 1px;
}}

/* ═══ 네비게이션 ═══ */
.nav {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(10,10,18,0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(201,169,110,0.15);
    padding: 14px 0;
    display: flex;
    justify-content: center;
    gap: 6px;
    flex-wrap: wrap;
}}

.nav-link {{
    color: var(--gray);
    text-decoration: none;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 8px 16px;
    border-radius: 20px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}}

.nav-link:hover {{
    color: var(--gold-light);
    border-color: var(--gold-dark);
    background: rgba(201,169,110,0.08);
}}

/* ═══ 섹션 ═══ */
.menu-section {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 80px 40px 40px;
}}

.section-header {{
    text-align: center;
    margin-bottom: 50px;
}}

.section-deco {{
    color: var(--gold);
    font-size: 16px;
    margin-bottom: 12px;
    opacity: 0.7;
}}

.section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: var(--gold-light);
    letter-spacing: 6px;
    text-transform: uppercase;
}}

.section-line {{
    width: 120px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 18px auto;
}}

.section-count {{
    font-size: 13px;
    color: var(--gray);
    font-weight: 300;
    letter-spacing: 2px;
}}

/* ═══ 메뉴 그리드 ═══ */
.menu-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
}}

/* ═══ 메뉴 카드 ═══ */
.menu-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}}

.menu-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gold-dark), var(--gold), var(--gold-dark));
    opacity: 0;
    transition: opacity 0.4s;
}}

.menu-card:hover {{
    transform: translateY(-8px);
    background: var(--bg-card-hover);
    border-color: var(--gold-dark);
    box-shadow:
        0 20px 60px rgba(0,0,0,0.5),
        0 0 40px rgba(201,169,110,0.08);
}}

.menu-card:hover::before {{
    opacity: 1;
}}

.card-image-wrap {{
    position: relative;
    overflow: hidden;
    aspect-ratio: 1;
}}

.card-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}

.menu-card:hover .card-image {{
    transform: scale(1.08);
}}

.image-shine {{
    position: absolute;
    top: 0; left: -100%;
    width: 50%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transition: left 0.6s;
}}

.menu-card:hover .image-shine {{
    left: 150%;
}}

.card-content {{
    padding: 20px 22px 24px;
    text-align: center;
}}

.item-name {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--white);
    margin-bottom: 10px;
    letter-spacing: 0.5px;
    line-height: 1.3;
}}

.item-price {{
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--gold);
    margin-bottom: 10px;
    text-shadow: 0 0 20px rgba(201,169,110,0.3);
}}

.item-desc {{
    font-size: 13px;
    color: var(--gray);
    font-weight: 300;
    line-height: 1.6;
    letter-spacing: 0.3px;
}}

/* ═══ 푸터 ═══ */
.footer {{
    text-align: center;
    padding: 60px 20px;
    border-top: 1px solid rgba(201,169,110,0.1);
    margin-top: 60px;
}}

.footer-logo {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: var(--gold);
    margin-bottom: 12px;
}}

.footer-text {{
    font-size: 13px;
    color: var(--gray);
    font-weight: 300;
    letter-spacing: 1px;
}}

/* ═══ 스크롤바 ═══ */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: var(--bg-dark); }}
::-webkit-scrollbar-thumb {{
    background: var(--gold-dark);
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{ background: var(--gold); }}

/* ═══ 인쇄용 ═══ */
@media print {{
    .nav {{ display: none; }}
    .menu-card {{ break-inside: avoid; }}
    .menu-section {{ page-break-before: always; }}
    body {{ background: #000 !important; }}
}}

/* ═══ 반응형 ═══ */
@media (max-width: 900px) {{
    .menu-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .cover-title {{ font-size: 48px; }}
    .section-title {{ font-size: 32px; }}
}}

@media (max-width: 600px) {{
    .menu-grid {{ grid-template-columns: 1fr; }}
    .cover-frame {{ padding: 30px 40px; }}
}}

/* ═══ 부드러운 등장 애니메이션 ═══ */
.menu-card {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}}

.menu-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}
</style>
</head>
<body>

<!-- 표지 -->
<div class="cover">
    <div class="cover-frame">
        <div class="cover-deco">· · · ✦ · · ·</div>
        <h1 class="cover-title">JooN's Sushi</h1>
        <div class="cover-subtitle">M E N U</div>
        <div class="cover-line"></div>
        <div class="cover-address">29910 Murrieta Hot Springs Rd L, Murrieta, CA</div>
        <div class="cover-url">joonssushimurrieta.com</div>
    </div>
</div>

<!-- 네비게이션 -->
<nav class="nav">
{nav_html}
</nav>

<!-- 메뉴 섹션 -->
{sections_html}

<!-- 푸터 -->
<div class="footer">
    <div class="footer-logo">JooN's Sushi</div>
    <div class="footer-text">Thank you for dining with us ✦ Open Daily</div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {{
    const observer = new IntersectionObserver(function(entries) {{
        entries.forEach(function(entry, i) {{
            if (entry.isIntersecting) {{
                const cards = entry.target.querySelectorAll('.menu-card');
                cards.forEach(function(card, idx) {{
                    setTimeout(function() {{ card.classList.add('visible'); }}, idx * 100);
                }});
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ threshold: 0.1 }});
    document.querySelectorAll('.menu-grid').forEach(function(grid) {{ observer.observe(grid); }});
}});
</script>
</body>
</html>'''

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nHTML 저장 완료: {OUTPUT_HTML}")
    print(f"   카테고리: {len(cats)}개")
    print(f"   메뉴 아이템: {len(menu)}개")


if __name__ == "__main__":
    menu = load_menu()
    generate_html(menu)
