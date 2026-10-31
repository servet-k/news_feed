import json
import os
import sys
import urllib.request

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# DÜZELTME: Orijinal RSS feed adresiniz tam isabetle tanımlandı!
target_rss_url = "https://ensonhaber.com"

print("GitHub Actions için RSS2JSON güvenli veri hattı kuruluyor...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # RSS adresinizi engellenmeyen küresel bir JSON/XML dönüştürücü tüneline gönderiyoruz
    tunnel_api = f"https://rss2json.com{target_rss_url}"
    
    req = urllib.request.Request(tunnel_api, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        json_data = json.loads(response.read().decode('utf-8'))
        
    # Mevcut feedparser döngünüzün (entry.get, entry.media_content vb.) 
    # kırılmaması için gelen JSON verisini feed nesnesine simüle ediyoruz
    if "items" in json_data and json_data["status"] == "ok":
        class MockFeed:
            def __init__(self, items):
                self.entries = []
                for item in items:
                    # XML yapısındaki media:content görsel mantığını birebir taklit ediyoruz
                    img_link = item.get("enclosure", {}).get("link", "") if item.get("enclosure") else ""
                    if not img_link and "thumbnail" in item:
                        img_link = item.get("thumbnail", "")

                    entry = {
                        "published": item.get("pubDate", ""),
                        "updated": item.get("pubDate", ""),
                        "title": item.get("title", ""),
                        "summary": item.get("description", ""),
                        "description": item.get("description", ""),
                        "link": item.get("link", ""),
                        "media_content": [{"url": img_link}] if img_link else []
                    }
                    
                    # Sözlük yapısını obje (.title, .link vb.) gibi okuyabilen sarmalayıcı sınıf
                    class Element:
                        def __init__(self, d): 
                            self.__dict__ = d
                        def get(self, k, default=""): 
                            return self.__dict__.get(k, default)
                            
                    self.entries.append(Element(entry))
        
        feed = MockFeed(json_data["items"])
    else:
        print("Hata: Tünel servisinden geçersiz yanıt alındı.")
        sys.exit(1)

except Exception as e:
    print(f"Veri tüneli kurulurken hata oluştu: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın korunan birebir aynısı
for entry in feed.entries:
    img_url = ""
    if 'media_content' in entry and len(entry.media_content) > 0:
        media = entry.media_content
        img_url = media.get('url', '') if hasattr(media, 'get') else media[0].get('url', '')
    
    data = {
        "time": entry.get('published', entry.get('updated', '')),
        "title": entry.get('title', ''),
        "content": entry.get('summary', entry.get('description', '')),
        "link": entry.get('link', ''),
        "img": img_url
    }
    
    print(f"Başarıyla Çekildi: {data['title']}")
    haber.append(data)

if len(haber) == 0:
    print("Hata: Dönüştürülen RSS içeriği boş veya işlenemedi.")
    sys.exit(1)

# JSON çıktısını kaydetme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 Harika! {len(haber)} adet haber RSS feed üzerinden başarıyla kaydedildi -> {output_file}")
