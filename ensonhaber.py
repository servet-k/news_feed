from get_feed import get_feed
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")
os.makedirs(output_dir, exist_ok=True)

def get_ensonhaber_from_homepage():
    """RSS 403 verdiği için ana sayfadan çekiyoruz"""
    url = "https://www.ensonhaber.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
    except Exception as e:
        print(f"Ana sayfa çekme hatası: {e}")
        return []

    haber_list = []
    
    # Ensonhaber ana sayfasındaki haber kartlarını bul
    # (Site yapısına göre selector'lar değişebilir, birkaç deneme yaptım)
    articles = soup.select("div.news-item, article, .haber, .item, .news, .card") or soup.find_all("a", href=True)

    seen_links = set()
    
    for article in articles:
        try:
            # Link
            link_tag = article if article.name == "a" else article.find("a", href=True)
            if not link_tag:
                continue
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.ensonhaber.com" + link
            
            if link in seen_links or "/rss" in link or "#" in link:
                continue
            seen_links.add(link)

            # Başlık
            title = link_tag.get_text(strip=True) or ""
            if not title or len(title) < 15:
                title_tag = article.find(["h1", "h2", "h3", "h4", "span", "p"])
                title = title_tag.get_text(strip=True) if title_tag else ""

            if not title or len(title) < 15:
                continue

            # Resim
            img = ""
            img_tag = article.find("img")
            if img_tag:
                img = img_tag.get("src") or img_tag.get("data-src") or img_tag.get("data-original") or ""
                if img and not img.startswith("http"):
                    img = "https://www.ensonhaber.com" + img

            # İçerik (kısa özet)
            content = ""
            desc_tag = article.find(["p", "span", "div"], class_=lambda x: x and ("desc" in x.lower() or "summary" in x.lower() or "spot" in x.lower()))
            if desc_tag:
                content = desc_tag.get_text(strip=True)

            data = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "title": title,
                "content": content,
                "link": link,
                "img": img
            }
            haber_list.append(data)

            if len(haber_list) >= 20:  # İstediğin kadar sınırla
                break

        except Exception:
            continue

    print(f"Ensonhaber ana sayfadan {len(haber_list)} haber çekildi")
    return haber_list


# Önce RSS'i dene, olmazsa ana sayfaya düş
url = "https://www.ensonhaber.com/rss/ensonhaber.xml"
haber = get_feed(url)

if not haber or len(haber) == 0:
    print("RSS boş veya 403, ana sayfadan çekiliyor...")
    haber = get_ensonhaber_from_homepage()

# Debug
for data in haber[:3]:
    print(data["title"])
    print(data["link"])
    print("---")

json_string = json.dumps(haber, indent=4, ensure_ascii=False)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)
