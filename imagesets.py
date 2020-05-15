

def get_soup(url,header):
    #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

query = "suffer"
query= query.split()
query='+'.join(query)
url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)

ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("a",{"class":"iusc"}):
    #print a
    #mad = json.loads(a["mad"])
    #turl = mad["turl"]
    m = json.loads(a["m"])
    murl = m["murl"]

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    #image = Image.open(urllib.request.urlopen(url))
    r = requests.get(murl,stream=True)
    try:
        image = Image.open(r.raw)
        width,height = image.size
        if(width > 1000 and height > 1000):
            print(width,height,murl)
            break
    except:
        pass
