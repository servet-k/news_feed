import json
import os
import sys
import urllib.request
import feedparser

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# ÇÖZÜM: Sizin oluşturduğunuz engelsiz resmi Google FeedBurner adresi!
my_feedburner_url = "https://feeds.feedburner.com/ensonhaber/xk7EWkSI4r8"

print("Oluşturulan FeedBurner proxy hattı üzerinden haber akışı senkronize ediliyor...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # GitHub Actions'ın engellenmediği Google altyapısına doğrudan istek açıyoruz
    req = urllib.request.Request(my_feedburner_url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as response:
        xml_data = response.read().decode('utf-8')
    
    # Gelen temiz ve dolu XML verisi orijinal feedparser kütüphanenize teslim ediliyor
    feed = feedparser.parse(xml_data)

except Exception as e:
    print(f"FeedBurner proxy bağlantı katmanında hata oluştu: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın birebir özgün hali (Hiçbir yapı bozulmadı)
for entry in feed.entries:
    img_url = ""
    # XML dosyasındaki <media:content url="..."> görsel bağını tam isabet yakalıyoruz
    if 'media_content' in entry and len(entry.media_content) > 0:
        img_url = entry.media_content.get('url', '')
    elif 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                img_url = link.get('href', '')
                break

    data = {
        "time": entry.get('published', entry.get('updated', '')),
        "title": entry.get('title', ''),
        "content": entry.get('summary', entry.get('description', '')),
        "link": entry.get('link', ''),
        "img": img_url
    }
    
    print(f"Başarıyla İşlendi: {data['title']}")
    haber.append(data)

if len(haber) == 0:
    print("Hata: Çekilen haber listesi boş döndü.")
    sys.exit(1)

# JSON çıktısını tam istediğiniz şablonda kaydetme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 Muhteşem! {len(haber)} adet güncel haber yeni tüneliniz üzerinden başarıyla kaydedildi -> {output_file}")
