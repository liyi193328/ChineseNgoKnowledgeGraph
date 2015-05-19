import os,pickle,json,pprint
from py2neo import Graph,Node,watch
province = ['北京市', '上海市', '天津市', '重庆市', '黑龙江省', '吉林省', '辽宁省', 
            '新疆维吾尔自治区', '甘肃省', '宁夏回族自治区', '山西省', '陕西省', '河南省', '河北省', '山东省', '西藏自治区', '四川省', 
            '青海省', '湖南省', '湖北省', '江西省', '安徽省', '江苏省', '浙江省', '福建省', '云南省', '贵州省', 
            '广西壮族自治区', '广东省', '海南省','内蒙古自治区', '香港特别行政区', '台湾', '澳门特别行政区'];
orgType = ["国内机构","境外机构","基金会","企业","政府部门"];
graph = Graph()
ans = []
time = range(2004,2016)
for year in time:
	yearTostr  = str(year)
	provinceYearNum = {}
	provinceYearNum['year'] = year
	provinceYearNum[yearTostr] = {}
	stat = ""
	for pro in province:
		proTostr = str(pro)
		provinceYearNum[yearTostr][proTostr] = {}
		par = {"province":pro}
		if year == 2004:#all
			par = {"province":pro}
			stat = "match (n:ngo) where n.province = {province} return count(n);"
			result = graph.cypher.execute(stat,par)
			cnt = result[0][0]
			provinceYearNum[yearTostr][proTostr]['total'] = int(cnt)
			for orgtype in orgType:
				orgtypeTostr = str(orgtype)
				stat = "match (n:ngo) where n.province = {province} and n.orgType = {orgtype} return count(n);"
				par = {"province":pro,"orgtype":orgtype}
				result = graph.cypher.execute(stat,par)
				cnt = result[0][0]
				provinceYearNum[yearTostr][proTostr][orgtypeTostr] = int(cnt)
		elif year == 2005:
			par = {"province":pro}
			stat = "match (n:ngo) where toInt(n.time) < 2006 and toInt(n.time) > 1000 and n.province = {province} return count(n);"
			result = graph.cypher.execute(stat,par)
			cnt = result[0][0]
			provinceYearNum[yearTostr][proTostr]['total'] = int(cnt)
			for orgtype in orgType:
				orgtypeTostr = str(orgtype)
				stat = "match (n:ngo) where toInt(n.time) < 2006  and toInt(n.time) > 1000 and n.province = {province} and n.orgType = {orgtype} return count(n);"
				par = {"province":pro,"orgtype":orgtype}
				result = graph.cypher.execute(stat,par)
				cnt = result[0][0]
				provinceYearNum[yearTostr][proTostr][orgtypeTostr] = int(cnt)
		else:
			par = {"province":pro,"year":year}
			stat = "match (n:ngo) where toInt(n.time) = {year} and n.province = {province} return count(n);"
			result = graph.cypher.execute(stat,par)
			cnt = result[0][0]
			provinceYearNum[yearTostr][proTostr]['total'] = int(cnt)
			for orgtype in orgType:
				orgtypeTostr = str(orgtype)
				stat = "match (n:ngo) where toInt(n.time) = {year} and n.province = {province} and n.orgType = {orgtype} return count(n);"
				par = {"province":pro,"orgtype":orgtype,"year":year}
				result = graph.cypher.execute(stat,par)
				cnt = result[0][0]
				provinceYearNum[yearTostr][proTostr][orgtypeTostr] = int(cnt)
	ans.append(provinceYearNum)
provinceYearNum = ans
fp = open("provinceYearNum.pkl","wb")
pickle.dump(provinceYearNum,fp)
fp.close()				
fp = open("provinceYearNum.pkl","rb")
provinceYearNum = pickle.load(fp)
print(type(provinceYearNum))
fp.close()
pprint.pprint(provinceYearNum)
fp = open(r"F:\research\Graduation\liyi\polls\static\data\provinceYearNum.json","wb")
s = json.dumps(provinceYearNum,ensure_ascii = False)
fp.write(s.encode("utf-8"))
fp.close()
print("end")

stat = "match (n:ngo) return n.name"
result = graph.cypher.execute(stat)
names = [ per[0] for per in result ]
names = {"nameAll":names}
print("begin to save:")
fp = open(r"F:\research\Graduation\liyi\polls\static\data\ngoName.json","wb")
s = json.dumps(names,ensure_ascii = False)
fp.write(s.encode("utf-8"))
fp.close()
print("end")
