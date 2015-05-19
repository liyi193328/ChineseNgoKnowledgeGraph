from getInfo import getInfo
import re
from bs4 import BeautifulSoup
from orgClass import NGO
from getOrgInfo import getOrgInfo
import time
import pickle

preSite = "http://www.ngo20map.com/Index/list_index?&p="
lastPage = 84
pat = re.compile('<a href="(.*)" target="_blank">(.*)</a>')
pre = "http://www.ngo20map.com/"
st = 1
cnt = 0
ngo = list()
for i in range(st,lastPage):
	print("page: %d\n" %i)
	# time.sleep(2)
	url = (preSite+str(i)).strip()
	html = getInfo(url)
	soup = BeautifulSoup(html)
	# print(soup)
	fSite = re.findall(pat,html)
	for j in range(0,len(fSite)):
		# time.sleep(0.5)
		cnt = cnt + 1
		orgurl = pre+fSite[j][0]
		print(orgurl)
		ngo.append( getOrgInfo(orgurl) )
		print("\n")
	print("\n")

print(cnt)
fp = open("orginfo.pkl","wb")
pickle.dump(ngo,fp)
fp.close()
