from head import *
import getInfo
from orgClass import NGO , perHire

def findHire(url,ngo,numHire):
	html = getInfo.getInfo(url)
	loc = 0
	while loc != -1:
		perhire = perHire()
		m = re.search(r'<td><a href="(.*)" title="(.+)" target= "_blank" class="it1">(.+)</a></td>',html[loc:])
		if m == None: break
		# perhire.urlLink = 
		perhire.post = m.group(3)

		loc = loc + m.end()
		m = re.search(r'<td>(.*)</td>',html[loc:])
		perhire.unit = m.group(1)
		loc =  loc + m.end()

		m = re.search(r'<td>(.*)</td>',html[loc:])
		perhire.worksite = m.group(1)
		loc =  loc + m.end()

		m = re.search(r'<td>(.*)</td>',html[loc:])
		perhire.updateTime = m.group(1)
		loc =  loc + m.end()

		# perhire.show()

		ngo.hire.append(perhire)
	return ngo
