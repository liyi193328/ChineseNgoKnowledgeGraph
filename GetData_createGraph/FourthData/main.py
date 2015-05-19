from getInfo import getInfo
import re
from bs4 import BeautifulSoup
from orgClass import NGO
from getOrgInfo import getOrgInfo
import time
import pickle,pprint

# preSite = "http://www.chinacsrmap.org/Org_List_CN.asp?LstFlt_Page="
preSite="http://www.chinacsrmap.org/Org_List_CN.asp?LstFlt_D1=2&LstFlt_Page="
orgPre = "http://www.chinacsrmap.org"
lastPage = 9 #total 9 pages
pat = re.compile(r'''<div class="teaserBox" onClick="location.href='(.*)';">''') # check or find every org's site
st = 1
cnt = 0
ngo = list()
# suf = ['?LstFlt_D1=2&LstFlt_Page=1','?LstFlt_D1=2&LstFlt_Page=2','?LstFlt_D1=2&LstFlt_Page=3',]
for i in range(st,lastPage):
	print("page: %d\n" %i)
	url = (preSite+str(i)).strip()
	html = getInfo(url)
	# print(url)
	# print(html)
	soup = BeautifulSoup(html)
	fSite = re.findall(pat,html)
	# print(url)
	# print(len(fSite))
	for j in range(0,len(fSite)):
		cnt = cnt + 1
		orgurl = orgPre + fSite[j]
		# print(orgurl)
		ngotem = getOrgInfo(orgurl)
		if ngotem != -1:
			ngo.append(ngotem)
		print("\n")
	print("\n")

print(cnt)
fp = open("orginfoFourthData.pkl","wb")
pickle.dump(ngo,fp)
fp.close()
