from bs4 import BeautifulSoup
import requests as rq
import os
from PIL import Image
import urllib.request

#ONLY CHANGE URL HERE
URL = "https://en.wikipedia.org/wiki/Julia_set"
#LOCAL DIRECTORY NAME FOR ALL IMAGES
dirName = "julia_set"

def getLinks(URL):
    #open link
    request = rq.get(URL)
    soup = BeautifulSoup(request.text, "html.parser")

    #find all /wiki/ shortcuts
    urls = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if url.find("/wiki/") == 0:
            urls.append(url)

    #clean up non relevant links
    bannedTerms = ["Help:", "Wikipedia:", "File:", "Portal:", "Special:", "Main_Page",
    "Help:Maintenance", "Category:", "Wikipedia:General", "Wikipedia:Community"]

    for term in bannedTerms:
        for x in urls:
            if term in x:
                urls.remove(x)
    
    #fill the URLS to make them usable
    fullURLs = []
    for l in urls:
        fullURLs.append("https://en.wikipedia.org" + l)

    for l in fullURLs:
        print(l)
        
    return fullURLs


def downloadImages(URL, dirName):
    #open url
    r2 = rq.get(URL)
    soup2 = BeautifulSoup(r2.text, "html.parser")

    #get image links
    links = []
    x = soup2.select('img')

    for img in x:
        links.append(img['src'])

    #clean up non relevant images
    bannedTerms = ["/static/images/footer/",
                   "CentralAutoLogin", "Wikiquote-logo", "footer", "wikihiero"]

    for term in bannedTerms:
        for x in links:
            if term in x:
                links.remove(x)

    #Final check to make sure links are created correctly
    fixedLinks = []

    for l in links:
        if("https:" not in l):
            fixedLinks.append("http:" + l)

    #create title of directory
    title = URL.lstrip("htps:/en.wikdaorg")
    os.makedirs("photos/" + dirName + "/" + title, exist_ok=True)

    #max amount of images to download per page
    i = 0

    #download images
    for index, img_link in enumerate(fixedLinks):
        if i <= 10:
            img_data = rq.get(img_link).content
            with open('photos/'+dirName+"/"+title+'/'+str(i+1)+'.png', 'wb+') as f:
                image = Image.open(urllib.request.urlopen(img_link))
                width, height = image.size
                if height > 30 and width > 30:
                    print("Downloading photo #" + str(i) + " from " + title)
                    f.write(img_data)
                    i+=1
        else:
            f.close()
            break


#function calls
links = getLinks(URL)
print("\nAll links successfully found.\nDownloading Images.\n")
for l in links:

    downloadImages(l, dirName)
print("Download(s) complete.")