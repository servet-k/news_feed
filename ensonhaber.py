import json
import os
import sys
import urllib.request
import feedparser
from urllib.parse import quote

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# ÇÖZÜM: Ensonhaber'in haberlerini GitHub Actions'ın asla engellemediği Google News üzerinden çekiyoruz!
google_news_rss = "https://google.com"

print("GitHub dostu Google News RSS havuzuna bağlanılıyor...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    # Doğrudan Google altyapısına güvenli bir ham istek açıyoruz
    req = urllib.request.Request(google_news_rss, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        xml_data = response.read().decode('utf-8')
    
    # Gelen temiz XML verisini mevcut feedparser kütüphanenize teslim ediyoruz
    feed = feedparser.parse(xml_data)

except Exception as e:
    print(f"Google servislerine bağlanılamadı: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın birebir aynısı (Hiçbir yapı bozulmadı)
for entry in feed.entries:
    # Google News kaynaklı başlıkların sonundaki " - Ensonhaber" kısmını temizliyoruz
    clean_title = entry.get('title', '')
    if " - Ensonhaber" in clean_title:
        clean_title = clean_title.split(" - Ensonhaber")[0].strip()

    data = {
        "time": entry.get('published', entry.get('updated', '')),
        "title": clean_title,
        "content": entry.get('summary', entry.get('description', '')),
        "link": entry.get('link', ''),
        "img": "" # Google News standart RSS akışında görsel sunmadığı için boş geçilir veya sitenin varsayılan logosu konabilir
    }
    
    print(f"Başarıyla Çekildi: {data['title']}")
    haber.append(data)

if len(haber) == 0:
    print("Hata: Google haber havuzundan veri alınamadı.")
    sys.exit(1)

# Mevcut JSON çıktı yapınızla birebir aynı şekilde kaydetme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 Muhteşem! {len(haber)} adet güncel haber Google News üzerinden başarıyla senkronize edildi -> {output_file}")
