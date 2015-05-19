import pickle,re
import urllib.request,urllib.parse
import json,pprint
from getAddFromBM import *

def getAddress(lines):
    # print(lines)
    if lines == "":
        return -1
    Ga = re.search(r"(.*)地址：(.*)([\n|\x20](.+) (.+))?\n",lines)
    if Ga:
        # print(Ga.group(0))
        if Ga.group(2):
            return Ga.group(2)
        else:
            return Ga.group(3)
    con = "联系方式："
    findCon = lines.find(con) #在介绍文字中查找联系方式
    if findCon != -1:
        lines = lines[findCon+len(con):len(lines)]
    else:
        Ga = re.search("\.{5,}",lines)
        if Ga:
            lines = lines[Ga.end():len(lines)]
    findLocList = lines.splitlines()
    for per in findLocList:
        #根据一个字符串判断是否是一个地址
        # print(per)
        if len(per) > 30:
            continue
        per = per.split()
        for stper in per:
            Ga = re.search(".*[省|市|县|街|区].*",stper)
            if Ga:
                return stper
            # if stper.find("省")!=-1 or stper.find("市") != -1 or stper.find("县")!= -1 or stper.find("街") or stper.find:
            #     return stper 
    return -1

with open("orginfoFinal.pkl","rb") as fp:
    ngo = pickle.load(fp)
    infoFromBaidu = {} #name is the key and ngo's info can't be gotten from baidu map, it has'nt the key and value
    l = len(ngo)
    print("len(ngo):",l)
    step = int(l/10)
    st = 0
    cnt = 0
    en = st + step
    # while(st < l):
    #     en = min(l,st+step)
    #     for i in range(st,en):
    #         perNgo = ngo[i]
    #         print(perNgo.name,"bfloc: " + perNgo.location)
    #         if perNgo.location== "":
    #             if perNgo.enName != "" and perNgo.connectionInfo != "":  #
    #                 f = getAddress(perNgo.description)
    #                 if f != -1:
    #                     perNgo.location = f

    #         print("firstFind: ",perNgo.location)

    #         if perNgo.location != "":
    #             (province,fAdd,perInfoFromBaidu) = getAddFromBM(perNgo.location)
    #             if fAdd != -1:
    #                 infoFromBaidu[perNgo.name] = perInfoFromBaidu
    #                 if province == perNgo.province:
    #                     perNgo.location = fAdd
    #                 if perNgo.province == "":
    #                     perNgo.province = province
    #         else:
    #             (province,fAdd,perInfoFromBaidu) = getAddFromBM(perNgo.name)
    #             if fAdd != -1:
    #                 infoFromBaidu[perNgo.name] = perInfoFromBaidu
    #             if perNgo.province != "" and province == perNgo.province:
    #                 perNgo.province = province
    #                 perNgo.location = fAdd

    #             elif perNgo.province == "" and fAdd != -1 and province != -1:
    #                 perNgo.province = province
    #                 perNgo.location = fAdd

    #         with open("orginfoFinalNew"+str(cnt)+".pkl","wb+") as fp:
    #             pickle.dump(ngo,fp)
    #             fp.close()
    #         with open("infoFromBaidu"+str(cnt)+".pkl","wb+") as fp:
    #             pickle.dump(infoFromBaidu,fp)
    #             fp.close()
    #         with open("infoFromBaidu"+str(cnt)+".json","wb+") as fp:
    #             fp.write(infoFromBaidu)
    #             fp.close()
    #         st = en
    cnt = 0
    for perNgo in ngo:
        print(cnt)
        cnt = cnt + 1
        print(perNgo.name,"bfloc: " + perNgo.location)
        if perNgo.location== "":
            if perNgo.enName != "" and perNgo.connectionInfo != "":  #
                f = getAddress(perNgo.description)
                if f != -1:
                    perNgo.location = f

        print("firstFind: ",perNgo.location)

        if perNgo.location != "":
            (province,fAdd,perInfoFromBaidu) = getAddFromBM(perNgo.location)
            if fAdd != -1:
                infoFromBaidu[perNgo.name] = perInfoFromBaidu
                if province == perNgo.province:
                    perNgo.location = fAdd
                if perNgo.province == "":
                    perNgo.province = province
        else:
            (province,fAdd,perInfoFromBaidu) = getAddFromBM(perNgo.name)
            if fAdd != -1:
                infoFromBaidu[perNgo.name] = perInfoFromBaidu
            if perNgo.province != "" and province == perNgo.province:
                perNgo.province = province
                perNgo.location = fAdd

            elif perNgo.province == "" and fAdd != -1 and province != -1:
                perNgo.province = province
                perNgo.location = fAdd
        
# print("info\n",type(infoFromBaidu),infoFromBaidu)
with open("orginfoFinalNew.pkl","wb+") as fp:
    pickle.dump(ngo,fp)
    fp.close()
print("begin to save:")
fpn = open("infoFromBaidu.pkl","wb")
pickle.dump(infoFromBaidu,fpn)
fpn.close()
print("end save")
