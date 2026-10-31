import json
import os
import sys
import feedparser

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# Orijinal ve doğru RSS besleme adresiniz doğrudan hedefleniyor
target_rss_url = "https://ensonhaber.com"

print("GitHub Actions yerleşik RSS motoru başlatılıyor...")

try:
    # feedparser kütüphanesinin kendi içindeki gizli User-Agent ve istek katmanını tetikliyoruz
    # requests/cloudscraper gibi bot olarak işaretlenen TLS parmak izlerini kullanmaz
    feed = feedparser.parse(
        target_rss_url,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

except Exception as e:
    print(f"Bağlantı motoru site duvarını aşamadı: {e}")
    sys.exit(1)

haber = []

# Sizin feedparser döngünüzün ve veri şemanızın korunan birebir aynısı
for entry in feed.entries:
    img_url = ""
    # XML dosyasındaki <media:content url="..."> görsel bağını yakalıyoruz
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

# Eğer boşa düşerse veya kısıtlanma devam ederse güvenli hata çıktısı
if len(haber) == 0:
    print("Hata: RSS içeriği boş döndü. Sitenin XML şeması veya erişim durumu kontrol edilmeli.")
    sys.exit(1)

# JSON çıktısını düzenli bir şekilde kaydetme
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 Harika! {len(haber)} adet güncel haber başarıyla kaydedildi -> {output_file}")
