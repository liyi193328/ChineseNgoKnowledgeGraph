from head import *
import getInfo 

def findImage(url):
	html = getInfo.getInfo(url)
	logo = re.search(r'<div class="ml_logo"><img width="230px" height="115px" src="(.*)" /></div>',html)
	return logo.group(1)
