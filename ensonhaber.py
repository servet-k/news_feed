import json
import os
import sys
import requests
import feedparser

output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

os.makedirs(output_dir, exist_ok=True)

# Sizin kullandığınız orijinal RSS adresi korundu
target_rss_url = "https://www.ensonhaber.com/rss/ensonhaber.xml"

print("GitHub Actions için RSS koruması tünellenerek aşılıyor...")

# feedparser'ın engellenmesini önlemek için tünel proxy adresi oluşturuluyor
proxy_url = f"https://scrape.do{target_rss_url}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # İstek doğrudan tünel üzerinden gerçek RSS linkine atılıyor
    response = requests.get(proxy_url, headers=headers, timeout=20)
    
    if response.status_code != 200:
        print(f"Proxy bağlantı hatası. Durum kodu: {response.status_code}")
        sys.exit(1)
        
    # Gelen gerçek XML verisi feedparser'a teslim ediliyor
    xml_content = response.text
    feed = feedparser.parse(xml_content)

except Exception as e:
    print(f"Bağlantı esnasında hata oluştu: {e}")
    sys.exit(1)

haber = []

# Sizin orijinal programınızdaki feedparser döngünüzün birebir aynısı:
for entry in feed.entries:
    img_url = ""
    # XML dosyasındaki <media:content url="..."> etiketini tam isabet yakalar
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
    
    # Konsol çıktısı doğrulaması
    print(f"Zaman: {data['time']}")
    print(f"Başlık: {data['title']}")
    print("-" * 20)
    
    haber.append(data)

if len(haber) == 0:
    print("Hata: RSS tünelden de boş döndü. Lütfen workflow loglarını inceleyin.")
    sys.exit(1)

# JSON formatına dönüştürme ve üzerine yazma
json_string = json.dumps(haber, indent=4, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"\n🚀 İşlem Başarılı! {len(haber)} adet haber RSS üzerinden çekilerek {output_file} dosyasına kaydedildi.")
