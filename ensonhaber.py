import json
import os
import sys
import urllib.request
import feedparser

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# Orijinal RSS adresiniz doğrudan hedefleniyor
target_rss_url = "https://ensonhaber.com"

print("GitHub Actions ham bağlantı motoru başlatılıyor (Direct urllib Socket)...")

# Sunucu korumasını aşmak için tarayıcı kimlik kartı oluşturuluyor
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

try:
    # requests yerine sunucu korumalarını bypass eden düşük seviyeli urllib isteği kuruluyor
    req = urllib.request.Request(target_rss_url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=30) as response:
        xml_data = response.read().decode('utf-8')
    
    # İndirilen ham XML verisi feedparser kütüphanenize teslim ediliyor
    feed = feedparser.parse(xml_data)

except Exception as e:
    print(f"Bağlantı motoru site duvarını aşamadı: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın birebir aynısı
for entry in feed.entries:
    img_url = ""
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
    
    print(f"Başarıyla Çekildi: {data['title']}")
    haber.append(data)

if len(haber) == 0:
    print("Hata: Çekilen veri ayrıştırılamadı, XML şablonu boş dönmüş olabilir.")
    sys.exit(1)

# JSON çıktısını kaydetme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 İşlem Başarılı! {len(haber)} adet güncel haber {output_file} dosyasına yazıldı.")
