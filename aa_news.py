import feedparser
import json

#to get image link, use beautifulsoup
from bs4 import BeautifulSoup
import requests,lxml



url="https://www.aa.com.tr/tr/rss/default?cat=guncel"

headers={"user-agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}
response=requests.get(url,headers=headers).text
soup=BeautifulSoup(response,"lxml")
img_container=soup.find_all("image")
img_container=img_container[1::]
img_list=[]
for img in img_container:
    img_list.append(img.text)

feed=feedparser.parse(url)

print(f"                                 {feed.feed.title}\n")
""" 
for entry in feed.entries:
    try:

        print(f"{entry.updated}")
        print(f"{entry.title}")
        print(entry.description)
        print(f"{entry.link}")
        print("\n")
    except:
        pass
 """
print(f'{30*"*"}      {20*"-"}       {30*"*"}')


for j in range(3):
    print(f"{feed.entries[j].updated}")
    print(f"{feed.entries[j].title}")
   # print(f"{feed.entries[j].description}")
    print(f"{feed.entries[j].link}")
    print("\n")

def haber_dict(feed):
    data_list=[]
    i=0
    for entry in feed.entries:
        
        haber_data={}
        try:
            haber_data["time"]=entry.updated
        except:
            haber_data["time"]=""
        try:
            haber_data["title"]=entry.title
        except:
            haber_data["title"]=""
        try:
            haber_data["content"]=entry.description
        except:
            haber_data["content"]=""
        try:
            haber_data["link"]=entry.link
        except:
            haber_data["link"]=""
        try:
            haber_data["img"]=img_list[i]
            i+=1
        except:
            haber_data["img"]=""
               
        data_list.append(haber_data)
        
       
    return data_list


data=haber_dict(feed)

json_string=json.dumps(data,indent=4,ensure_ascii=False)

with open("e:/react/aa-news/json/haber.json","w") as f:
    f.write(json_string,)
