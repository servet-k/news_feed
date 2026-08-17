import feedparser
import requests

def get_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.ensonhaber.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Feed çekme hatası ({url}): {e}")
        return []

    # Debug için (Actions log'unda göreceksin)
    print(f"URL: {url}")
    print(f"Status: {getattr(response, 'status_code', 'N/A')}")
    print(f"Bozo: {feed.bozo}")
    if feed.bozo:
        print(f"Bozo Exception: {feed.bozo_exception}")
    print(f"Entry sayısı: {len(feed.entries)}")

    haber_list = []
    for entry in feed.entries:
        # Zaman
        time = getattr(entry, "updated", None) or getattr(entry, "published", None) or ""
        
        # Başlık
        title = getattr(entry, "title", "") or ""
        
        # İçerik
        content = getattr(entry, "description", None) or getattr(entry, "summary", None) or getattr(entry, "content", [{}])[0].get("value", "") if getattr(entry, "content", None) else ""
        
        # Link
        link = getattr(entry, "link", "") or ""
        
        # Resim (daha sağlam kontrol)
        img = ""
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            img = entry.media_thumbnail[0].get("url", "")
        elif hasattr(entry, "media_content") and entry.media_content:
            img = entry.media_content[0].get("url", "")
        elif hasattr(entry, "enclosures") and entry.enclosures:
            img = entry.enclosures[0].get("href", "") or entry.enclosures[0].get("url", "")
        # Bazı feedlerde image alanı farklı yerde olabilir
        elif hasattr(entry, "image") and isinstance(entry.image, dict):
            img = entry.image.get("href", "") or entry.image.get("url", "")

        data = {
            "time": time,
            "title": title,
            "content": content,
            "link": link,
            "img": img
        }
        haber_list.append(data)

    return haber_list
