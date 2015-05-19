from head import *
import difflib
from py2neo import Graph, Node, Relationship, Path, Rev, authenticate
from py2neo.cypher import cypher_escape
import re
# s = os.path.dirname(os.getcwd())
# print(s)
# with open(s+r"\GetData\orginfoFormat.pkl","rb") as fp:
# 	ngoData = pickle.load(fp)

orgType = ["全部","国内机构","境外机构","基金会","企业","政府部门"]
provinceNameMap = {"西藏省":"西藏自治区","内蒙省":"内蒙古自治区","广西省":"广西壮族自治区",
                    "新疆省":"新疆维吾尔自治区","宁夏省":"宁夏回族自治区"}
fp = open("orginfoFinalNew.pkl", "rb")
ngo = pickle.load(fp)
print(len(ngo))

authenticate("localhost:7474", "neo4j", "liyi193328")
graph = Graph()
# graph.delete_all()

def getAllNgoName():
    fp = open("orginfoFinalNew.pkl", "rb")
    ngo = pickle.load(fp)
    names = list()
    for per in ngo:
        names.append(per.name)
    fp = open("AllNgoName.pkl","wb")
    pickle.dump(names,fp)
    fp.close()
    return names

def findNode(pat,names):
    if len(pat) < 2:
        return None
    mostSim = -1
    maxAns = 0
    for name in names:
        if pat in name:
            mostSim = 1
            maxAns = name
            break
        sim = difflib.SequenceMatcher(None,pat,name).ratio()
        if sim > mostSim:
            mostSim = sim
            maxAns = name
    # print(maxAns,mostSim)
    if mostSim >= 0.85:
        result = graph.cypher.execute("match (n:ngo{name:{name}}) return id(n),n.name;",{"name":maxAns})
        return result
    else:
        return None

def buildNode(perNgo):
    if perNgo.scale == None:
        perNgo.scale = ""
    if perNgo.esTime == None:
        perNgo.esTime = 0
    if perNgo.connectionInfo == None:
        perNgo.connectionInfo = ""
    if perNgo.province in provinceNameMap:
        perNgo.province = provinceNameMap[perNgo.province]
    time = perNgo.esTime
    Ga = re.search(r'\d+',str(time))
    if Ga:
        perNgo.esTime = int(Ga.group(0))
    partners = ""
    for w in perNgo.partners:
        partners += w + "，"
    sponsors = ""
    for w in perNgo.sponsors:
        sponsors += w + "，"

    statement = "merge (nodeNgo:ngo{name:{Name}, enName: {EnName},location:{ Location},connectionInfo:{ConnectionInfo},\
        time:{Time},scale: {Scale},personCharge: {PersonCharge},orgType:{OrgType},province:{Province},\
        description:{ Description }, field:{Field}, partners:{ Partners },sponsors: { Sponsors } } ) return nodeNgo;"
    tx.append(statement,{"Name":perNgo.name, "EnName": perNgo.enName, "Location":perNgo.location,"Time":perNgo.esTime,
        "PersonCharge":perNgo.personCharge,"OrgType":perNgo.orgType,"Province":perNgo.province,"ConnectionInfo":perNgo.connectionInfo,
        "Scale":perNgo.scale, "Description":perNgo.description,"OrgType":perNgo.orgType,"Field":perNgo.field,
        "Partners": {partners},"Sponsors":{sponsors}
        })

    if perNgo.orgType != "":
        tx.append("match (nodeNgo:ngo{name:{Name} }),(n:orgType) \
            where n.OrgType={orgType} merge (nodeNgo)-[r:机构类型]->(n) return r;"
            ,{"Name":perNgo.name,"orgType":perNgo.orgType}
        )

    if perNgo.connectionInfo != "" and perNgo.connectionInfo != None:
        # print(perNgo.connectionInfo)
        tx.append("merge (temp:connectionInfo { connectionInfo:{ connectionInfo },name:{ Name } } )",{"connectionInfo":perNgo.connectionInfo,"Name":perNgo.name})
        tx.append("match (nodeNgo:ngo{name:{Sname} }) ,(temp:connectionInfo { name:{ Name } } )\
            merge (nodeNgo)-[r:联系信息]->(temp)\
            return r;"
            ,{"Sname":perNgo.name, "Name": perNgo.name}
        )

    if perNgo.field != [] and perNgo.field != None:
        for perField in perNgo.field:
            if perField.strip() == "":
                pass
            tx.append("merge (temp:field { Field:{ PerField } } )",{"PerField":perField})
            tx.append("match ( nodeNgo:ngo{name:{Sname} } ),(temp:field{ Field:{ Sfield } } ) \
                merge (nodeNgo)-[r:领域]->(temp)\
                return r;",
                {"Sname":perNgo.name,"Sfield":perField}
            )

    if perNgo.esTime != 0 and perNgo.esTime != "" and perNgo.esTime != None:
        tx.append("merge (tem: time { EsTime:{esTime} } );",{"esTime":perNgo.esTime})
        tx.append("match (nodeNgo {name: {Sname} }),( tem:time{EsTime:{esTime} } )\
            merge (nodeNgo)-[r:成立时间]->(tem)\
            return r;",
            {"Sname":perNgo.name,"esTime":perNgo.esTime}
        )

    if perNgo.province != "" and perNgo.province != None:
        tx.append("merge (tem: province { Province:{province} } );",{"province":perNgo.province})
        tx.append("match (nodeNgo {name: {Sname} }),( tem:province{Province:{province} } )\
            merge (nodeNgo)-[r:省份]->(tem)\
            return r;",
            {"Sname":perNgo.name,"province":perNgo.province}
        )

def buildNodeRel(perNgo):
    for partner in perNgo.partners:
        if len(partner) < 30 and len(partner) >= 2:  #限定名字小于30
            nodesID = findNode(partner,names) #find NGO whose name most similiar to partner
            print(perNgo.name, "partner: ",partner,"nodesID:",nodesID)
            if nodesID != None:
                nodeID = nodesID[0][0]
                tx.append("match (nodeNgo:ngo{ name:{Name} }),(partner:ngo) \
                    where id(partner) = {nodeID}\
                    merge (nodeNgo)-[r:合作伙伴]-> (partner)\
                    return r;",
                    {"Name":perNgo.name,"nodeID":nodeID }
                )
            else:
                tx.append("merge (n:partners {name:{name} })return n;",{"name":partner})
                tx.append("match (nodeNgo:ngo{ name:{Name} }),(sponsor:sponsors{name:{partner_name}}) \
                    merge (nodeNgo)<-[r:合作伙伴]- (sponsor)\
                    return r;",
                    {"Name":perNgo.name,"partner_name":partner}
                )

    for sponsor in perNgo.sponsors:
        if len(sponsor) < 30 and len(sponsor) >= 2:  #limit sponsor's len to 30
            nodesID = findNode(sponsor,names)
            print(perNgo.name, "sponsor: ",sponsor,"nodesID:",nodesID)
            if nodesID != None:
                nodeID = nodesID[0][0]
                tx.append("match (nodeNgo:ngo{ name:{Name} }),(sponsor:ngo) \
                    where id(sponsor) = {nodeID}\
                    merge (nodeNgo)<-[r:资助]- (sponsor)\
                    return r;",
                    {"Name":perNgo.name,"nodeID":nodeID }
                )
            else:
                tx.append("merge (n:sponsors{name:{name} } ) return n;",{"name":sponsor})
                tx.append("match (nodeNgo:ngo{ name:{Name} }),(sponsor:sponsors{name:{sp_name}}) \
                    merge (nodeNgo)<-[r:资助]- (sponsor)\
                    return r;",
                    {"Name":perNgo.name,"sp_name":sponsor}
                )

def createOrgType():
    st = "merge (n:orgType{OrgType:{orgType}});"
    for per in range(1,len(orgType)):
        tx.append(st,{"orgType":orgType[per]})

names = getAllNgoName()
tx = graph.cypher.begin()
print("begin to creat orgType:")
createOrgType()
print("end")
print("begin to build nodes")
for node in ngo:
    buildNode(node)
tx.process()
tx.commit()

print("begin to build rel(partner and sponsor):")
tx = graph.cypher.begin()
for node in ngo:
    buildNodeRel(node)
tx.process()
tx.commit()
