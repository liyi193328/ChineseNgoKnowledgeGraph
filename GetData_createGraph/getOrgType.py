from getOrgNumber import getOrgNumber
import pickle,os,re

urlPagef = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type="
urlPageS = "&field_type=0&area_type=0&province_type=0&market_type=0&keywords=&org_search=&page="
# urlPagef = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type=0\
# &field_type=0&area_type=1&orgType_type="
# urlPageS = "&market_type=0&keywords=&org_search=&page="
prefix = r'http://www.chinadevelopmentbrief.org.cn/org'
fileSiteList = "orgType.txt"
seq = ['0','1', '2', '3', '4','5']

orgType = ["全部","国内机构","境外机构","基金会","企业","政府部门"]
			
fp = open("orginfo_add_province.pkl","rb")
ngo = pickle.load(fp)
print("len(ngo): %d" %len(ngo))

cnt = 0
Pages = 0
orgNum = set()

for i in range(1,len(orgType)):
	print(orgType[i])
	url = urlPagef + str(seq[i]) +  urlPageS
	(orgNumTem,pages) = getOrgNumber(url,prefix,fileSiteList)
	Pages  += pages
	for per in orgNumTem:
		orgNum.add((per,i))
print("size_orgNum:",len(orgNum),Pages)

for perOrgNum in orgNum:
	for perNgo in ngo:
		if perNgo.orgNumber == perOrgNum[0]:
			perNgo.orgType = orgType[ perOrgNum[1] ]
			cnt = cnt + 1

print("cnt:",cnt)

print("writting to orginfo_add_orgType.pkl")
with open("orginfo_add_orgType.pkl","wb") as fp:
	pickle.dump(ngo,fp)
print("succ to write!")
fp.close()

