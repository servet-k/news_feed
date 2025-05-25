from get_feed import get_feed
import json
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

all_url="https://www.sciencedaily.com/rss/all.xml"

all=get_feed(all_url)

json_string=json.dumps(all,indent=4,ensure_ascii=False)
with open(f"e:/react/aa-news/json/science.json","w") as f:
        f.write(json_string)

for haber in all:
    print(haber["time"])
    print(haber["title"])
    print(haber["content"])
    print(haber["link"])
    print("\n")