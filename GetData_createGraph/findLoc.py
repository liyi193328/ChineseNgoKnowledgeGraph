from getInfo import getInfo
from head import *

def findLoc(url):
	html = getInfo(url)
	locG = re.search(r"var content = '(.*)'",html)
	return locG.group(1).strip()

# s = findLoc("http://www.chinadevelopmentbrief.org.cn/org30/org_map/")
# print(s)