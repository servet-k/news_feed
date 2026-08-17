import feedparser
import cloudscraper

def get_feed(url):
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )

    try:
        response = scraper.get(url, timeout=25)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Feed çekme hatası ({url}): {e}")
        return []

    print(f"URL: {url}")
    print(f"Status: {response.status_code}")
    print(f"Bozo: {feed.bozo}")
    if feed.bozo:
        print(f"Bozo Exception: {feed.bozo_exception}")
    print(f"Entry sayısı: {len(feed.entries)}")

    haber_list = []
    for entry in feed.entries:
        time = getattr(entry, "updated", None) or getattr(entry, "published", None) or ""
        title = getattr(entry, "title", "") or ""
        content = (
            getattr(entry, "description", None)
            or getattr(entry, "summary", None)
            or (getattr(entry, "content", [{}])[0].get("value", "") if getattr(entry, "content", None) else "")
        )
        link = getattr(entry, "link", "") or ""

        img = ""
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            img = entry.media_thumbnail[0].get("url", "")
        elif hasattr(entry, "media_content") and entry.media_content:
            img = entry.media_content[0].get("url", "")
        elif hasattr(entry, "enclosures") and entry.enclosures:
            img = entry.enclosures[0].get("href", "") or entry.enclosures[0].get("url", "")

        data = {
            "time": time,
            "title": title,
            "content": content,
            "link": link,
            "img": img
        }
        haber_list.append(data)

    return haber_list
