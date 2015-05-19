from django.db import models
from py2neo import Node, Relationship, Graph,watch, authenticate
import logging,re,pickle
import json,pprint
# Create your models here.

#mainly use word parse and so on to handle the  input search
#searchInfo: "org_tye",""
def handleInput(searchInfo):
    return searchInfo

def performatData(data,type):
	s = data.replace("\t", "").replace("\xa0","").replace("&nbsp;","").splitlines()
	tem = []
	for j in range(0,len(s)):
		if s[j] != "":
			if len(s[j]) > 50 and type == 'connectionInfo':
				l = int(len(s[j])/2)
				tem.append(s[j][0:l]+'\n')
				tem.append(s[j][l: len(s[j])] + '\n')
			else:
				tem.append(s[j] + '\n')
	data = ''.join(tem)
	st = data.strip()
	xi = re.findall(r'&(.*);',st)
	for j in xi:
		st = st.replace(j,"")
	data = st
	return data
def formatData(nodes):
	for perNode in nodes:
		connectioninfo =  perNode.get('connectionInfo')
		description = perNode.get('description')
		if connectioninfo:
			perNode['connectionInfo'] = performatData(connectioninfo,"connectionInfo")
		if description:
			perNode['description'] = performatData(description,"description")
	return nodes

# get data from neo4j accroding to predata
def communicate(preData):
	authenticate("localhost:7474", "neo4j", "liyi193328")
	graph = Graph()
	# watch("py2neo.cypher")
	# watch("httpstream")
	nodes = []
	links = []
	porgType = r'(.*)'+preData['orgType']+r'(.*)'
	pfield = r'(.*)'+preData['field']+r'(.*)'
	pprovince= r'(.*)'+preData['province']+r'(.*)'
	porgNameA = r'(.*)'+preData['nameA']+r'(.*)'
	porgNameB = r'(.*)' + preData['nameB'] + r'(.*)'
	count = 0
	flag = 0
	if(preData['nameB'] == ""): #find ngos
		flag = 0
		par = {
			"orgType":porgType,
			"field":pfield,
			"province":pprovince,
			"name":porgNameA
			}
		result = graph.cypher.execute("match (n:ngo)-[r:领域]->(m:field) where n.orgType =~ {orgType} and m.Field =~ {field} \
			and n.province =~ {province} and n.name =~ {name} return distinct n,id(n),labels(n) limit 20;"
			,par)
		for per in range(0,len(result)):
			# tem = json.loads( json.dumps(result[per][0].properties) )
			tem = result[per][0].properties
			tem['nodesID'] = int(result[per][1])
			tem['nodesLabels'] = result[per][2]
			nodes.append(tem)
		temRe = graph.cypher.execute("match (n:ngo)-[r:领域]->(m:field) where n.orgType =~ {orgType} and m.Field =~ {field} \
			and n.province =~ {province} and n.name =~ {name} return distinct count(distinct n);",par)
		count = temRe[0][0]

	else:
		flag = 1
		par = {
			"nameA":preData['nameA'],
			"nameB":preData['nameB']
		}
		stat = "match p = (A:ngo)-[*..4]-(B:ngo) where A.name = {nameA} and B.name = {nameB} return nodes(p),relationships(p) order by length(p) limit 5;"
		result = graph.cypher.execute(stat,par)
		write("result_relation",str({"result": result,"par":par}))
		nodesID = []
		for row in result:
			onePathnodes = row[0]
			for ngo in onePathnodes:
				[node,ID] = convertNodeToSend(ngo)
				if ID not in nodesID:
					nodes.append(node)
					nodesID.append(ID)
			for rel in row[1]:
				startID = findRefID( rel.start_node.ref )
				endID = findRefID( rel.end_node.ref )
				source = -1
				target = -1
				for i,j in enumerate(nodesID):
					if j == startID:
						source = i
					if j == endID:
						target = i
				if source != -1 and target != -1:
					links.append({"source":source,"target":target,"type":rel.type})
		# stat = "match p = (A:ngo)-[*..4]-(B:ngo) where A.name = {nameA} and B.name = {nameB} return count(p);"
		# temRe = graph.cypher.execute(stat,par);
		# count = temRe[0][0]
	nodes = formatData(nodes)
	data = {'nodes':nodes,'links':links,"count":count,"flag":flag}
	write("dataSearch.json",str(data))
	return data
def findRefID(st):
	return int( re.search(r"node/(\d+)",st).group(1) )
def convertNodeToSend(ngo):
	node = ngo.properties
	# nodesID = re.search(r"node/(\d+)",ngo.ref).group(1)
	nodesID = findRefID(ngo.ref)
	node['nodesID'] = nodesID
	node['nodesLabels'] = ngo.labels
	return node,nodesID
 #convert data form neo4j to what can be used to render using d3 
def getFinal(rawData):
	return rawData

def mainHandle(searchInfo):
	preData = handleInput(searchInfo)
	rawData = communicate(preData)
	finalData = getFinal(rawData)
	return finalData

#handle the node extend
def getNode(ID):
	authenticate("localhost:7474", "neo4j", "liyi193328")
	graph = Graph()
	nodes = []
	result = graph.cypher.execute("match (n:ngo) where id(n) = {id} return n,labels(n);",{"id":ID})
	if len(result) != 0:
		data = {}
		data = result[0][0].properties;
		data['nodesLabels'] = result[0][1];
		data['nodesID'] = ID
		nodes.append(data)
		return {"nodes":nodes,"links":[]}

def getProvinceTime(province,time):
	authenticate("localhost:7474", "neo4j", "liyi193328")
	graph = Graph()
	if province == "":
		province = '.*'
	data = []
	if time == 2004:
		ngoList = graph.cypher.execute("match (n:ngo) where n.province =~ {province} return id(n),n.name;",{"province":province})
	elif time == 2005:
		ngoList = graph.cypher.execute("match (n:ngo) where n.province =~ {province} and toInt( n.time ) < 2006 return id(n),n.name;",{"province":province})
	else:
		ngoList  =graph.cypher.execute("match (n:ngo) where n.province =~ {province} and n.time = {time} return id(n),n.name;",{"province":province,"time":time})
	for perNgo in ngoList:
		row = {}
		row["id"] = perNgo[0]
		row['name'] = perNgo[1]
		data.append(row)
	return data

def write(filename,obj):
	fp = open(filename,"w+",encoding = "utf-8")
	fp.write(obj)
	fp.close()

def updateData(dataSet,updateNodeID,id): #updateNodeID is the id of updating node in graph, id is the id in dataSet's nodes
	authenticate("localhost:7474", "neo4j", "liyi193328")
	graph = Graph()

	id = int(id)
	par = {"ID":int(updateNodeID)}
	result1 = graph.cypher.execute("match (n) -[r]-> (m) where id(n) = {ID} return type(r),m,id(m),labels(m) limit 10;",par)
	result2 = graph.cypher.execute("match (m) -[r]-> (n) where id(n) = {ID} return type(r),m,id(m),labels(m) limit 10;",par) #limit the 

	# print(result1)
	# print(result2)
	#covert results to json fromat
	# logging.info(type(dataSet))
	# write("result1.txt",str(result1) )
	# write("result2.txt",str(result2) )

	nodes = dataSet['nodes']
	links = dataSet['links']
	nodesID = [ w['nodesID'] for w in nodes]

	print("nodesID",nodesID)

	# write("links.txt",str(links))
	tem = []
	if links != {} or links != None:
		for link in links:
			tem.append({"source":link['source']["index"],"target":link['target']["index"],"type":link["type"]})
		links = tem
	# write("linksAF.txt",str(links))

	l = len(nodes)
	l1 = len(result1)
	l2 = len(result2)
	for i in range(0,l1):
		if result1[i][2] not in nodesID:
			# print(result1[i])
			tem = result1[i][1].properties
			tem['nodesID'] = int(result1[i][2])#this node'id in graph
			tem['nodesLabels'] = result1[i][3]
			node_ID = result1[i][2]
			nodesID.append(node_ID)
			nodes.append(tem)
			source = id
			newl = len(nodes)-1  # not consider the last node
			thisNodeID = newl
			links.append({"source":source,"target":thisNodeID,"type":result1[i][0]})
			for j in range(0,newl):
				if j != id:
					par = {"beforeID":nodesID[j],"ID":node_ID}
					statement = "match (n) -[r] -> (m) where id(n) = {beforeID} and id(m) = {ID} return type(r);"
					tem = graph.cypher.execute(statement,par)
					if len(tem) != 0:
						links.append({"source":j , "target":thisNodeID,"type":tem[0][0]})
					statement = "match (n)-[r]->(m) where id(n) = {ID} and id(m) = {beforeID} return type(r);"
					tem = graph.cypher.execute(statement,par)
					if len(tem) != 0:
						links.append({"source":thisNodeID, "target":j,"type":tem[0][0]})

	l = len(nodes)

	for i in range(0,l2):
		if result2[i][2] not in nodesID:
			tem = result2[i][1].properties
			tem['nodesID'] = int(result2[i][2])#this node'id in graph
			tem['nodesLabels'] = result2[i][3]
			node_ID = result2[i][2]
			nodesID.append(node_ID)  
			nodes.append(tem)
			source = id
			newl = len(nodes)-1
			thisNodeID=newl
			links.append({"source":thisNodeID,"target":id,"type":result2[i][0]})
			for j in range(0,newl):
				if j != id:
					par = {"beforeID":nodesID[j],"ID":node_ID}
					statement = "match (n) -[r] -> (m) where id(n) = {beforeID} and id(m) = {ID} return type(r);"
					tem = graph.cypher.execute(statement,par)
					if len(tem) != 0:
						links.append({"source":j , "target":thisNodeID,"type":tem[0][0]})
					statement = "match (n)-[r]->(m) where id(n) = {ID} and id(m) = {beforeID} return type(r);"
					tem = graph.cypher.execute(statement,par)
					if len(tem) != 0:
						links.append({"source":thisNodeID, "target":j,"type":tem[0][0]})
						
	nodes = formatData(nodes)
	nodes = json.loads(json.dumps(nodes))
	links = json.loads(json.dumps(links))
	finalResult = {"nodes":nodes,"links":links}
	write("result",str(finalResult))
	return finalResult

# pare = {
# 	"orgType":"",
# 	"field":"",
# 	"province":"北京市",
# 	"orgName":""
# 	}
# data = communicate(pare)
# pprint.pprint(data)
# data = json.loads(json.dumps(data))
# # updateData(data,data['nodes'][3].nodesID,3)
# pprint.pprint(  updateData(data,data['nodes'][3]['nodesID'],3)  )

# getNode(2180)