from head import *
import getInfo
from orgClass import *

from bs4 import BeautifulSoup
import pprint

def replace_with_newlines(element):
    # print(element)
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br' or elem.name == "p":
            text += '\n'
    return text

def getOrgInfo(url):
    ngo = NGO()
    ngo.url = url
    url = url.strip()
    html = getInfo.getInfo(url)
    soup = BeautifulSoup(html)
    # print(soup.prettify())

    if soup.find("h3"):
        title = soup.find("h3")
        if title.get_text() != "":
            ngo.name = title.get_text().splitlines()[0]
        print(ngo.name)

        content = title.find_next_siblings("p")
        s = ""
        encontent = soup.find("p",class_ = "sch_con2 l")

        if content != []:
            per = content[0]
            # print(per.prettify())
            for w in per.find_all("p"):
                s += replace_with_newlines(w) + "\n"

            if per.find_all("div"):
                totalDiv = per.find_all("div")
                for w in totalDiv:
                    s += w.get_text()+"\n"

            if encontent != None and encontent.find("b"):
                enb =encontent.find("b")
                ngo.enName = enb.get_text()

            ngo.description = s
            # print(s)

            #format 
            # tem = list()
            lines = ngo.description.replace("\t", "").replace("\xa0"," ").splitlines()
            # lines = ngo.description.splitlines()
            # print(lines)

            if ngo.name != "" and re.search('[a-zA-Z]',ngo.name[0]):
                ngo.name,ngo.enName = ngo.enName,ngo.name

            ngo.sponsors = []
            for i in range(0,len(lines)):
                Ga = re.search(".*资助者$",lines[i])
                if Ga:
                    for j in range(i+1,len(lines)):
                        if lines[j] == "" and j<len(lines)-1 and ( lines[j+1] == "" or re.search( "(.*)合作",lines[j+1] ) ):
                            for k in range(i+1,j):
                                if lines[k] != "":
                                    Ga = re.search("（.*）",lines[k])
                                    if Ga:
                                        lines[k] = lines[k].replace(Ga.group(0),"")
                                    if "、" in lines[k]:
                                        words = lines[k].split("、")
                                    elif "；" in lines[k]:
                                        words = lines[k].split("；")
                                    elif "," in lines[k]:
                                        words = lines[k].split(",")
                                    elif "，" in lines[k] or "," in lines[k]:
                                        words = lines[k].split("，")
                                    else:
                                        words = lines[k].split(" ")
                                    for q in words:
                                        if q:
                                            # print(q)
                                            ngo.sponsors.append(q)
                            break
                    break

            ngo.partners = []
            for i in range(0,len(lines)):
                Ga = re.search(".*合作伙伴$",lines[i])
                if Ga:
                    for j in range(i+1,len(lines)):
                        if lines[j] == "" and j <len(lines)-1 and ( lines[j+1] == "" or re.search("(.*)独特性",lines[j+1]) ):
                            for k in range(i+1,j):
                                if lines[k] != "":
                                    # print("lines: ",lines[k])
                                    Ga = re.search("（.*）",lines[k])
                                    if Ga:
                                        lines[k] = lines[k].replace(Ga.group(0),"\n")
                                    # print("lines: ",lines[k])
                                    if "、" in lines[k]:
                                        words = lines[k].split("、")
                                        # print(words)
                                    elif "；" in lines[k]:
                                        words = lines[k].split("；")
                                    elif "," in lines[k]:
                                        words = lines[k].split(",")
                                    elif "，" in lines[k] or "," in lines[k]:
                                        words = lines[k].split("，")
                                    else:
                                        words = lines[k].split(" ")
                                    for q in words:
                                        if q:
                                            # print(q)
                                            ngo.partners.append(q)
                            break
                    break
                    
            Ga = re.search("(.*)地址[：|:](.*)\n(.*)",ngo.description)
            if Ga:
                if Ga.group(2):
                    ngo.location = Ga.group(2)
                else:
                    ngo.location = Ga.group(3)
                if " " in ngo.location:
                    ngo.location = ngo.location.split(" ")[0]

            Ga = re.search("负责人[：|:](.*)",ngo.description)
            if Ga:
                ngo.personCharge = Ga.group(1)
            Ga = re.search("员工人数[:|：](.*)",ngo.description)
            if Ga:
                ngo.scale = Ga.group(1)
            Ga = re.search("成立时间[：|:](.*)",ngo.description)
            if Ga:
                ngo.esTime = Ga.group(1)

            print(ngo.name,ngo.location,ngo.personCharge,ngo.scale,ngo.esTime,ngo.partners,ngo.sponsors)

    return ngo

# getOrgInfo("http://www.lvngo.com/ngo-18839-1.html")中文名和英文名交换
# getOrgInfo("http://www.lvngo.com/ngo-24261-1.html")
# getOrgInfo("http://www.lvngo.com/ngo-37038-1.html")
# getOrgInfo("http://www.lvngo.com/ngo-39933-1.html")
# getOrgInfo("http://www.lvngo.com/ngo-18601-1.html")


