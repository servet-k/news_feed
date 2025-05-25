
from get_feed import get_feed
import json
url="https://www.ensonhaber.com/rss/ensonhaber.xml"

haber=get_feed(url)

#for item in haber:
#    item["content"]=item["content"].split(">")[-1]

for data in haber:
    print(data["time"])
    print(data["title"])
    print(data["content"])
    print(data["link"])
    print(data["img"])
    print("\n")


json_string=json.dumps(haber,indent=4,ensure_ascii=False)

with open("e:/react/aa-news/json/ensonhaber.json","w") as f:
    f.write(json_string)
