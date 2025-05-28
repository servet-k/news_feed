import os,json
import ssl
from get_feed import get_feed


output_dir = os.path.join(os.path.dirname(__file__), "json")
#output_file = os.path.join(output_dir, "json")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

urls={"daily":"https://www.dailymail.co.uk/articles.rss",
      "sun":"https://www.thesun.co.uk/news/worldnews/feed/",
      "mirror":"https://www.mirror.co.uk/news/world-news/?service=rss",
      "express":"https://feeds.feedburner.com/daily-express-world-news",
      "bbc":"https://feeds.bbci.co.uk/news/world/rss.xml" ,
      "cezire":"https://www.aljazeera.com/xml/rss/all.xml",
      "telegraph":"https://www.telegraph.co.uk/rss.xml",
      "New_York_Times":"https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    
}

for key,values in urls.items():
    data=get_feed(values)
    if values=="https://feeds.feedburner.com/daily-express-world-news":
        for item in data:
            item["content"]=item["content"].split(">")[-1]
    json_string=json.dumps(data,indent=4,ensure_ascii=False)
    
    with open(f"{output_dir}/{key}.json","w") as f:
        f.write(json_string)

