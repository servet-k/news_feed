import feedparser
def get_feed(url):
  
  feed=feedparser.parse(url)
  haber_list=[]
  for entry in feed.entries:
        try:
            time=entry.updated or entry.published
        except:
            time=""
        try:
            title=entry.title
        except:
            title=""
        try:
            content=entry.description or entry.summary
        except:
            content=""
        try:
            link=entry.link
        except:
            link=""
        try:
          img=entry.media_thumbnail[0]["url"] 
        except:
          try:
            img=entry.media_content[0]["url"] 
          except:
            try:
              img=entry.enclosures[0]["href"]
            except:
                img=""

        data={"time":time,
                  "title":title,
                  "content":content,
                   "link":link ,
                   "img":img }
        haber_list.append(data)
  return haber_list
