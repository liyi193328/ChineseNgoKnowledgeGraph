from getOrgNumber import getOrgNumber
from getOrgInfo import getOrgInfo
import pickle,time
fieldName = ['全部', ' 劳工', '环保与动保', '三农/社区发展与救灾', '教育', '健康与防艾', 
                '性别与性少数', '老人与儿童', '残障', '社会创新/社会企业', 
                '能力建设/研究/支持/咨询', '民族/宗教/文化/艺术', 
                '企业社会责任', '社工', '其他']

urlPage = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?\
org_type=0&field_type=0&area_type=0&province_type=0&market_type=0&keywords=&org_search=&page="
prefix = r'http://www.chinadevelopmentbrief.org.cn/org'
fileSiteList = "Pages.txt"

# getOrgNumber(urlPage,prefix,fileSiteList)
fp = open(fileSiteList, "r", encoding="utf-8")
orgSiteList = fp.readlines()
l = len(orgSiteList)
fp.close()

tem = list()
times = 10
st = 0
step = int(l/times)
en = step
cnt = 0
while st < l:
	en = min(st+step,l)
	print("st,en: %d %d\n"%(st,en))
	t = getOrgInfo(st,en,orgSiteList)
	for i in t:
		tem.append(i)
	st = en
	cnt = cnt + 1

ngo = tem

newNgo = list()
for i in range(0,len(ngo)):
  if(ngo[i].name != ""):
    flag = False
    for j in range(i+1,len(ngo)):
      if(ngo[i].name == ngo[j].name):
        flag = True
        break
    if flag == False:
        newNgo.append(ngo[i])

print("ngo Item: %d" %len(newNgo))
print("writing to orginfo_new.pkl!")
with open("orginfo_new.pkl","wb") as fp:
  pickle.dump(newNgo,fp)
print("succ!")
fp.close()

