import os,pickle,json,pprint
from py2neo import Graph,Node,watch

graph = Graph()

# time = range(2000,2016)
# result = graph.cypher.execute("match (n:ngo) where toInt(n.time) < 2000 and toInt(n.time) > 1000 return count(n);")
# print(result[0][0])
# for year in time:
# 	result = graph.cypher.execute("match (n:ngo) where n.time = {year} return count(n);",{"year":year})
# 	print(result[0][0])

province = ['北京市', '上海市', '天津市', '重庆市', '黑龙江省', '吉林省', '辽宁省', 
            '新疆维吾尔自治区', '甘肃省', '宁夏回族自治区', '山西省', '陕西省', '河南省', '河北省', '山东省', '西藏自治区', '四川省', 
            '青海省', '湖南省', '湖北省', '江西省', '安徽省', '江苏省', '浙江省', '福建省', '云南省', '贵州省', 
            '广西壮族自治区', '广东省', '海南省','内蒙古自治区', '香港特别行政区', '台湾', '澳门特别行政区'];
st = {}
for pro in province:
	par = {"province":pro}
	stat = "match (n:ngo) where n.province = {province} return count(n);"
	result = graph.cypher.execute(stat,par)
	st[pro] = result[0][0]
items = st.items()
li = [ [v[1],v[0]] for v in items ]
li.sort()
li = [ [ li[i][1],li[i][0] ] for i in range(0,len(li))]
for per in li:
	print(per)
# fp = open(r"provinceYearNum.pkl","rb")
# data = pickle.load(fp)
# for per in data:
# 	total = 