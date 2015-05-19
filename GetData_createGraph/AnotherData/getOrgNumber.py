from head import *
import getInfo
import findOrg

def getOrgNumber(urlPage,prefix,filename):
	
	result = set()
	print("getting org number:")
	html = getInfo.getInfo(urlPage)
	# print(html)
	G = re.search(r'org_type=0&field_type=0&area_type=0&province_type=0&market_type=0&keywords=&org_search=&page=(\d+)">末页</a>',html)
	# print(G.group(0))
	if G:
		lastPage = int(G.group(1))
	else:
		 lastPage = 2

	print("last: %d" % lastPage)
	for i in range(1, lastPage):
		url = urlPage + str(i)
		print("for: %d" %i)
		# fp = open(str(i)+".html","w",encoding = "utf-8")
		html = getInfo.getInfo(url)
		# fp.write(html)
		# fp.close()
		result = result.union(findOrg.findOrg(html))
	tmp = list(result)[:]
	tmp.sort()
	result = tmp

	print("writing org number to %s..." %filename)
	fp = open(filename,"w+",encoding = "utf-8")
	for i in result:
		fp.write(prefix+str(i)+"/"+'\n')
	fp.close()
	print("succ writing  to %s!" %filename)

	return result

