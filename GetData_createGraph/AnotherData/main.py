from getInfo import getInfo
import re
from bs4 import BeautifulSoup
from orgClass import NGO
from getOrgInfo import getOrgInfo
import time
import pickle

preSite = "http://baike.lvngo.com/baike/chinango/index.php?page="
lastPage = 33
pat = re.compile('<a href="(.*)" target="_blank" class="xi2"(.*)</a>')
st = 1
cnt = 0
ngo = list()
for i in range(st,lastPage):
	print("page: %d\n" %i)
	url = (preSite+str(i)).strip()
	html = getInfo(url)
	soup = BeautifulSoup(html)
	fSite = re.findall(pat,html)
	for j in range(0,len(fSite)):
		cnt = cnt + 1
		orgurl = fSite[j][0]
		print(orgurl)
		ngo.append( getOrgInfo(orgurl) )
		print("\n")
	print("\n")

print(cnt)
fp = open("orginfoAnotherChina.pkl","wb")
pickle.dump(ngo,fp)
fp.close()
