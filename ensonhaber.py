
from get_feed import get_feed
import json
import os



output_dir = os.path.join(os.path.dirname(__file__), "json")
output_file = os.path.join(output_dir, "ensonhaber.json")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)


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

with open(output_file,"w") as f:
    f.write(json_string)
