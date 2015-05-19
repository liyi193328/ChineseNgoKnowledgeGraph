from head import *
import getInfo
from orgClass import *

from bs4 import BeautifulSoup
import pprint

fields = {"反腐败和透明化":"反腐败和透明化","艺术和文化":"民族/宗教/文化/艺术",
    "教育":"教育","环境":"环保与动保","金融和社会责任投资":"企业社会责任","健康和安全":"健康与防艾",
    "慈善事业":"慈善事业","社会标准和劳工保护（供应链）":"劳工",
    "妇女儿童":"老人与儿童","能源":"能源","气候变化":"气候变化",
    "社区":"三农/社区发展与救灾","生物多样性":"生物多样性","其他":"其他"
    }
def replace_with_newlines(element):
    # print(element)
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br' or elem.name == 'p' or elem .name == 'div': #合作伙伴的信息是包裹在这三个元素中的
            text += '\n'
    return text

def getOrgInfo(url):
    ngo = NGO()
    url = url.strip()
    html = getInfo.getInfo(url)
    soup = BeautifulSoup(html)
    # print(soup.prettify())
    kinddiv = soup.find("div",text="类别 : ")
    if kinddiv:
        kind = kinddiv.parent.find("div",class_ = "OrgInfodataItemContent").get_text()
        print(kind)
        if kind != '非政府组织':
            return -1
    namediv = soup.find("div",text="名称 : ")
    if namediv:
        name = namediv.parent.find("div",class_ = "OrgInfodataItemContent").get_text()
        print(name)
        ga = re.search(r'(([(|（].*[)|）]))',name)
        if ga:
            name = name.replace(ga.group(1),"")
        ngo.name = name
        print(name)
    timediv = soup.find("div",text="成立日期 : ")
    # print(timediv)
    if timediv:
        timestr = timediv.parent.find("div",class_ = "OrgInfodataItemContent").get_text()
        if re.search("(\d+)",timestr):
            time = int( re.search("(\d+)",timestr).group(1) ) 
            ngo.esTime = time
            print(time)

    fi = soup.find("div",text = re.compile("工作领域.*"))
    if fi:
        fie = fi.find_next("div",class_ = "OrgInfodataItemContent")
        if fie:
            ngo.field = [fields[i] for i in replace_with_newlines(fie).splitlines()]
    print(ngo.field)

    des = soup.find("div",text = re.compile("成立背景.*"))
    if des:
        descri = des.find_next("div",class_="OrgInfoSectionContent")
        if descri:
            ngo.description = descri.get_text()
            # print(ngo.description)
    des = soup.find("div",text = re.compile(("在中国的CSR项目.*")))
    if des:
        descri = des.find_next("div",class_="OrgInfoSectionContent")
        if descri:
            ngo.description += replace_with_newlines(descri)
    # print(ngo.description)

    partnersdiv = soup.find("div",text=re.compile(".*主要合作伙伴.*"))
    if partnersdiv:
        partnerstr = replace_with_newlines( partnersdiv.find_next("div",class_="OrgInfoSectionContent") ).splitlines()
        # print(partnerstr)
        tem = list()
        for w in partnerstr:
            if "，" in w:
                for q in w.split("，"):
                    if q.find("\uf0fc") == -1 and q.find("-") == -1:
                        tem.append(q)
            if "、" in w:
                for q in w.split("、"):
                    if q.find("\uf0fc") == -1 and q.find("-") == -1:
                        tem.append(q)
            else:
                for q in w.split():
                    if q.find("\uf0fc") == -1 and q.find("-") == -1:
                        tem.append(q)
        ngo.partners = tem
        if ngo.partners != []:
            s = ngo.partners[len(ngo.partners)-1]
            if s[len(s)-1] == "等":
                ngo.partners[len(ngo.partners)-1] = s.replace(s[len(s)-1],"")
        # print(ngo.partners)

    return ngo

# getOrgInfo("http://www.chinacsrmap.org/Org_Show_CN.asp?ID=1479")


