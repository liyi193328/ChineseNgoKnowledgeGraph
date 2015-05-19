from head import *
import getInfo
import findOrg

def getOrgNumber(urlPage,prefix,filename):
	
	result = set()
	print("getting org number:")
	html = getInfo.getInfo(urlPage)
	# print(html)
	G = re.search(r'page=(\d+)">末页</a>',html)
	# print(G.group(0))
	if G:
		lastPage = int(G.group(1))
	else:
		 lastPage = 2

	print("lastPage: %d" %lastPage)

	for i in range(1, lastPage):
		url = urlPage + str(i)
		# print(url)
		print("for: %d" %i)
		html = getInfo.getInfo(url)
		print("html get suc!")
		result = result.union(findOrg.findOrg(html))
	tmp = list(result)[:]
	tmp.sort()
	result = tmp
	# print("result: ",result)
	# print("writing org number to %s..." %filename)
	# fp = open(filename,"w+",encoding = "utf-8")
	# for i in result:
	# 	fp.write(prefix+str(i)+"/"+'\n')
	# fp.close()
	# print("succ writing  to %s!" %filename)

	return result,lastPage-1	

# getOrgNumber("","/org", "province.txt")
