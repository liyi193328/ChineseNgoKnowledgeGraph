import orgClass
import getInfo
from head import *
import findActive
import findImage
import findLoc

def getOrgInfo(start,end,orgSiteList):
    s1 = r'<div class="ml_name mt15">'
    s2_1 = r'<h1>'
    s2_2 = r'</h1>'
    s3_1 = r'<font>'
    s3_2 = r'</font>'
    name = enName = esTime = location = field = scale = description = info = recruit = image = ""
    suff = ["org_active/","org_hire/","org_image/","org_map/"]

    ans = list()

    for st in range(start,end):
        print("seq: %d" %st)
        url = orgSiteList[st].strip()
        ngo = orgClass.NGO()
        print(url[url.find(r'/org'):len(url)-1])
        orgNumber = int( url[url.find(r'/org')+len('/org'):len(url)-1] ) 
        # print(orgNumber)

        ngo.orgNumber = orgNumber

        html = getInfo.getInfo(url)
        loc = html.find(s1)
        if loc != -1:
            x = html.find(s2_1, loc + len(s1))
            if x == -1:
                continue
            y = html.find(s2_2, x + len(s2_1))
            if y == -1:
                continue
            ngo.name = html[x + len(s2_1):y]
            m = html.find(s3_1, y + len(s2_2))
            if m == -1:
                continue
            n = html.find(s3_2, m + len(s3_1))
            if(n == -1):
                continue
            ngo.enName = html[m + len(s3_1):n]

            Gr = re.search(r'<li><font>成立时间：</font>(\d*)年</li>', html[n:])
            if Gr.group(1):
                ngo.esTime = int(Gr.group(1))
            print("year: %d" %ngo.esTime)

            Ga = re.search(r'<li><font>工作领域：</font>(.*)</li>', html[Gr.end():])
            if Ga.group(1):
                field = Ga.group(1)
                ngo.field = field.split(" ")

            print(ngo.field)

            Gr = re.search(r'<li><font>机构规模：\s{0,10}</font>(.*)</li>', html[Ga.end():])
            if Gr.group(1):
                ngo.scale = Gr.group(1)
            print(ngo.scale)

            Ga = re.search(r'<div class="jgjs mt20">(.*)>',html[Gr.end():]) 
            # s = Ga.group(0)
            # print(s)
            x = Gr.end() + Ga.end()
            sec = html.find(r"</",x)
            ngo.description = html[x:sec]  #description
            # print(ngo.description)

        ngo.image = findImage.findImage(url + suff[2])
        # print(ngo.image)
        ngo.location = findLoc.findLoc(url+suff[3])
        print("location: %s"%ngo.location)

        # ngo.show()
        ans.append(ngo)

    return ans








