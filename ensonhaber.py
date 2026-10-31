import json
import os
import sys
import cloudscraper
import feedparser

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# Orijinal RSS besleme adresiniz tam isabetle korundu
target_rss_url = "https://ensonhaber.com"

print("Cloudscraper bot engeli aşma motoru yükleniyor...")

try:
    # GitHub Actions sunucusunu tamamen gerçek bir Chrome tarayıcıya dönüştürüyoruz
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    print(f"RSS akışı güvenli katmandan indiriliyor: {target_rss_url}")
    # Donmayı engellemek için kesin timeout sınırı (15 saniye) koyuyoruz
    response = scraper.get(target_rss_url, timeout=15)
    
    if response.status_code != 200:
        print(f"Hata: Sunucu bağlantıyı reddetti. Durum kodu: {response.status_code}")
        sys.exit(1)
        
    # İndirilen temiz XML içeriği feedparser'a hafızadan teslim ediliyor
    xml_data = response.text
    feed = feedparser.parse(xml_data)

except Exception as e:
    print(f"Bağlantı katmanında beklenmeyen bir hata oluştu: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın korunan birebir aynısı
for entry in feed.entries:
    img_url = ""
    # XML dosyasındaki <media:content> görsel bağını yakalıyoruz
    if 'media_content' in entry and len(entry.media_content) > 0:
        img_url = entry.media_content[0].get('url', '')
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
    print("Hata: Çekilen RSS şablonunun içi boş veya ayrıştırılamadı.")
    sys.exit(1)

# JSON formatında çıktı üretme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 Muhteşem! {len(haber)} adet güncel haber başarıyla sisteme işlendi -> {output_file}")
