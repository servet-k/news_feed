from get_feed import get_feed
import json,os
import ssl



output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "science.json")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

all_url="https://www.sciencedaily.com/rss/all.xml"

all=get_feed(all_url)

json_string=json.dumps(all,indent=4,ensure_ascii=False)
with open(output_file,"w") as f:
        f.write(json_string)

for haber in all:
    print(haber["time"])
    print(haber["title"])
    print(haber["content"])
    print(haber["link"])
    print("\n")