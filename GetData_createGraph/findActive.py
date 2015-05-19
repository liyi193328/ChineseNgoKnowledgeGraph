from head import *
import getInfo

def findActive(url):
	html = getInfo.getInfo(url)
	m = re.search(r'<div class="flxx">(.*)</div>',html)
	return m.group(1)

# x =findActive('http://www.chinadevelopmentbrief.org.cn/org30/org_active/')
# print(x)
