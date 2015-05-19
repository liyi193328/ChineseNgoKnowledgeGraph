from head import *
import getInfo
from orgClass import *

from bs4 import BeautifulSoup
def getOrgInfo(url):
    ngo = NGO()
    url = url.strip()
    html = getInfo.getInfo(url)
    soup = BeautifulSoup(html)
    # print(soup)

    ngo.name = soup.find(id="org-header").find("h1").get_text()
    print(ngo.name)

    location = soup.find("h3",text = "办公地址")
    ngo.location = location.findNextSibling("p").get_text()
    print("location: %s" %ngo.location)

    connInfoList = soup.find("h3",text = "联系方式").find_next_siblings("p")
    tem = list()
    for x in connInfoList:
        s = x.get_text().replace(" ","").replace("\n","")
        # print(s)
        # s = x.get_text().replace(" ","").replace("\n"," ").replace("\r","")
        if s == "访问机构网站":
            s = "网站: " + x.a['href']
        tem.append(s)
    ngo.connectionInfo = tem
    # print("connectionInfo: ",ngo.connectionInfo)

    tem = soup.find("span",text = "成立时间: ")
    if tem:
        tem = tem.find_parent("p").get_text()
        Ga = re.search("(\d*)年",tem)
        if Ga:
            if Ga.group(1):
                ngo.esTime = int( Ga.group(1))#year
                print("year: %d" %ngo.esTime )

    Ga = re.search("<span>全职人数: </span>(\d*)",html)
    if Ga:
        if Ga.group(1):
            ngo.scale = int(Ga.group(1)) #scale
            print("scale: %d" %ngo.scale)
    return ngo

# getOrgInfo("http://www.ngo20map.com/User/view/id/1764")







