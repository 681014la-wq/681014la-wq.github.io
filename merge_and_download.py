import json
import os
import re
import urllib.request

# Configuration
BASE_DIR = r"c:\joon_toy\joon_menu"
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[^\w\-_\. ]', '_', name).strip().replace(" ", "_").lower()

def clean_text(text):
    if text:
        return text.replace("(O)", "").strip()
    return ""

import ssl

def download_image(url, filename):
    if not url or url == "MISSING_IMAGE" or url is None:
        return None
    try:
        local_path = os.path.join(IMAGE_DIR, filename + ".jpg")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Referer': 'https://joonssushimurrieta.com/'
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        except ssl.SSLCertVerificationError:
            print(f"  SSL 인증서 오류 - 안전하지 않은 연결로 재시도: {url}")
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        return f"images/{filename}.jpg"
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

# Combined Data Initialization
final_menu = []

# Load Chunk 1 & 2
try:
    with open(os.path.join(BASE_DIR, "chunk1.json"), "r", encoding='utf-8') as f:
        final_menu.extend(json.load(f))
    with open(os.path.join(BASE_DIR, "chunk2.json"), "r", encoding='utf-8') as f:
        final_menu.extend(json.load(f))
except Exception as e:
    print(f"Error loading chunks: {e}")

# Data from scratchpad_9byhjhms.md (The 6 missing categories)
missing_categories_data = [
  {
    "category": "FROM THE SUSHI BAR(O)",
    "items": [
      { "name": "Chirashi(O)", "price": "$20.50", "description": "Assorted sashimi 12 pieces. Served over sushi rice. Served with miso soup, salad.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/5ed45529-47a3-49b1-bfd7-c0097f84c91a?w=320&fit=cover" },
      { "name": "Sashimi A(O)", "price": "$23.50", "description": "Tuna, salmon, and yellowtail sashimi. Served with rice upon request. Served with three pieces of each fish. Served with miso soup, salad.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/b3ba632e-5077-4f61-adfe-b283947a2f13?w=320&fit=cover" },
      { "name": "Sashimi B(O)", "price": "$25.50", "description": "Tuna, salmon, yellowtail and escolar sashimi. Served with rice upon request. Served with three pieces of each fish. Served with miso soup, salad.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/ef160846-2fd5-4583-a92d-cb0bfe4a4ac1?w=320&fit=cover" },
      { "name": "Sashimi C(O)", "price": "$30.50", "description": "Tuna, salmon, yellowtail, escolar, and albacore sashimi. Served with rice upon request. Served with three pieces of each fish. Served with miso soup, salad.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/6063b439-1770-429a-88cf-e8f77c1ac6c8?w=320&fit=cover" },
      { "name": "Unagi Special(O)", "price": "$20.50", "description": "Unagi and avocado served with rice. Served with miso soup and salad.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/2f60b8a5-0a42-429c-8ca7-f8c8d4561780?w=320&fit=cover" }
    ]
  },
  {
    "category": "SAUCES(O)",
    "items": [
      { "name": "Eel Sauce(O)", "price": "$0.50", "description": "Eel sauce is a thick, sweet sauce primarily made from soy sauce.", "image_url": None },
      { "name": "Ponzu(O)", "price": "$0.50", "description": "With a citrus-based sauce.", "image_url": None },
      { "name": "Salad Dressing(O)", "price": "$0.50", "description": "A blend typically featuring soy sauce, ginger, sesame.", "image_url": None },
      { "name": "Spicy Mayo(O)", "price": "$0.50", "description": "A cream-based sauce with chili sauce.", "image_url": None },
      { "name": "Sriracha(O)", "price": "$0.50", "description": "Thai-style hot sauce.", "image_url": None },
      { "name": "Wasabi(O)", "price": "$0.50", "description": "A pungent Japanese horseradish paste.", "image_url": None }
    ]
  },
  {
    "category": "SPECIAL ROLLS(O)",
    "items": [
      { "name": "JooN's Special Roll(O)", "price": "$17.50", "description": "Spicy crab, shrimp tempura peppered albacore on top with garlic ponzu, spicy mayo, eel sauce, sriracha, and potato crunchies.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/ec0f07cc-8180-4a33-b9e7-6f67261803b2?w=320&fit=cover" },
      { "name": "Mango Tango Roll(O)", "price": "$16.50", "description": "Salmon, avocado mango, mango sauce, red onion, shichimi, and sriracha on top.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/928cf7ec-e81e-452c-881c-e9a64f21647a?w=320&fit=cover" },
      { "name": "Mexican Roll(O)", "price": "$16.50", "description": "Spicy crab, avocado, cucumber shrimp and avocado on top with spicy mayo.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/36f1f76a-8a7e-4047-bd62-8465deed2489?w=320&fit=cover" },
      { "name": "Double Shrimp Roll(O)", "price": "$17.50", "description": "Crab, avocado, shrimp tempura shrimp and avocado on top.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/14402c96-2d13-4a1b-a561-4270cf051d65?w=320&fit=cover" },
      { "name": "Red Dragon Roll(O)", "price": "$17.50", "description": "Spicy tuna, shrimp tempura tuna on top with garlic ponzu and potato crunchies.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/c9f825ac-148a-4381-b68d-c7406f166a51?w=320&fit=cover" },
      { "name": "Caterpillar Roll(O)", "price": "$16.50", "description": "Crab, eel avocado on top with eel sauce.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/7658d77d-cde4-41d5-ad99-4ac277a2309b?w=320&fit=cover" },
      { "name": "Spring Roll(O)", "price": "$16.50", "description": "Crab, shrimp, spicy tuna wrapped in cucumber topped with green onion, masago, and ponzu sauce.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/781bb497-1bbb-4b6c-8ddc-015f69c7b370?w=320&fit=cover" },
      { "name": "Arigato Roll(O)", "price": "$14.50", "description": "Spicy tuna, albacore spicy albacore on top with garlic ponzu and potato crunchies.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/5673713e-7612-4fc9-8994-ff907859f936?w=320&fit=cover" }
    ]
  },
  {
    "category": "SPICY ROLLS(O)",
    "items": [
      { "name": "Taste Like My Ex-Girl Fried Roll(O)", "price": "$15.50", "description": "Spicy crab, avocado salmon and red onion on top with house spicy sauce.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/3ac274e0-3c6a-4a7c-b26e-5924a2de6cf9?w=320&fit=cover" },
      { "name": "Spicy Rainbow Roll(O)", "price": "$14.50", "description": "Spicy crab, avocado assorted fish on top.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/5673713e-7612-4fc9-8994-ff907859f936?w=320&fit=cover" },
      { "name": "Sex on the Beach Roll(O)", "price": "$15.50", "description": "Spicy crab, avocado peppered albacore on top.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/781bb497-1bbb-4b6c-8ddc-015f69c7b370?w=320&fit=cover" },
      { "name": "3 Alarm on Fire Roll(O)", "price": "$14.50", "description": "Spicy crab, avocado white fish on top with house spicy sauce.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/eab52563-0952-48c8-8903-403b69284c6d?w=320&fit=cover" }
    ]
  },
  {
    "category": "SUSHI(O)",
    "items": [
      { "name": "Yellowtail Sushi(O)", "price": "$9.50", "description": "Thinly sliced yellowtail on a bed of vinegared sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/074e7aee-7b42-406b-b9be-91645886c9d6?w=320&fit=cover" },
      { "name": "Salmon Egg Sushi(O)", "price": "$8.50", "description": "Glazed salmon roe atop vinegared rice, wrapped in crisp seaweed.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/b9cf8d8d-d578-4f0a-b132-5d448cc3ea90?w=320&fit=cover" },
      { "name": "Tuna Sushi(O)", "price": "$8.50", "description": "A slice of fresh tuna atop vinegared rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/63e76c47-c197-4ade-a1bb-b9d2ff317769?w=320&fit=cover" },
      { "name": "Smoked Paprika Salmon Sushi(O)", "price": "$8.50", "description": "Smoked salmon seasoned with paprika, includes sushi rice and nori.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/f7750e43-ad0c-4cf7-b909-25f3002c6547?w=320&fit=cover" },
      { "name": "Shrimp Sushi(O)", "price": "$6.50", "description": "Boiled shrimp on seasoned sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/17941733-da4f-4ccf-ba16-93da0b881c8f?w=320&fit=cover" },
      { "name": "Halibut Sushi(O)", "price": "$8.50", "description": "Thinly sliced halibut on sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/c13dc8a9-be49-49ec-94b9-02babced581a?w=320&fit=cover" },
      { "name": "Escolar Sushi(O)", "price": "$8.50", "description": "Escolar on sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/d1dd1b0c-5ff9-4005-8834-a7fb5bd1e23a?w=320&fit=cover" },
      { "name": "Octopus Sushi(O)", "price": "$7.50", "description": "Octopus on sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/68ddfe3e-ee0e-402f-8eee-7402d192367c?w=320&fit=cover" },
      { "name": "Salmon Sushi(O)", "price": "$7.50", "description": "Salmon on sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/0c0a9253-9684-448e-b537-a4acdebfb78d?w=320&fit=cover" },
      { "name": "Albacore Sushi(O)", "price": "$8.50", "description": "Albacore on sushi rice.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/6063b439-1770-429a-88cf-e8f77c1ac6c8?w=320&fit=cover" }
    ]
  },
  {
    "category": "TEMPURA ROLLS(O)",
    "items": [
      { "name": "Golden Tiger Cut Roll(O)", "price": "$15.50", "description": "Shrimp tempura, avocado, cream cheese fried spicy crab on top.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/d1dd1b0c-5ff9-4005-8834-a7fb5bd1e23a?w=320&fit=cover" },
      { "name": "Golden California Cut Roll(O)", "price": "$10.50", "description": "Deep fried california roll.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/68ddfe3e-ee0e-402f-8eee-7402d192367c?w=320&fit=cover" },
      { "name": "Popcorn Scallop Cut Roll(O)", "price": "$16.50", "description": "California roll topped with fried scallops.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/0c0a9253-9684-448e-b537-a4acdebfb78d?w=320&fit=cover" },
      { "name": "Oishi Cut Roll(O)", "price": "$13.50", "description": "Eel, crab, avocado, cream cheese and deep fried.", "image_url": "https://joonssushimurrieta.com/pluto-images/funnel/images/7b4d7620-e555-4c26-a76d-66ca6e8ba3dd?w=320&fit=cover" }
    ]
  }
]

# Convert missing_categories_data to individual items and add to final_menu
for cat in missing_categories_data:
    category_name = clean_text(cat["category"])
    for item in cat["items"]:
        item["category"] = category_name
        final_menu.append(item)

# Deduplicate and Clean
processed_items = []
seen_names = set()

for item in final_menu:
    name = clean_text(item.get("name", ""))
    cat = clean_text(item.get("category", ""))
    price = item.get("price", "")
    desc = item.get("description", "")
    url = item.get("image_url", "")
    
    if name and name not in seen_names:
        # Generate local path and download
        sanitized_name = sanitize_filename(name)
        local_path = download_image(url, sanitized_name)
        
        processed_items.append({
            "category": cat,
            "name": name,
            "price": price,
            "description": desc,
            "local_image": local_path,
            "original_url": url if url != "MISSING_IMAGE" else None
        })
        seen_names.add(name)

# Save Final JSON
output_path = os.path.join(BASE_DIR, "menu.json")
with open(output_path, "w", encoding='utf-8') as f:
    json.dump(processed_items, f, indent=2, ensure_ascii=False)

print(f"Finalized menu.json with {len(processed_items)} items.")
