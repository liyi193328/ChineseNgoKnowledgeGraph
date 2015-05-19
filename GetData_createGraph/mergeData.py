import pickle,sys,os,pprint
import difflib
# pprint.pprint(sys.path)
#merge name,location,year,conntioninfo
fp = open("orginfo_add_orgType.pkl","rb")
# fpn = open(os.path.dirname(__file__)+"\MoreData\orginfo_merge.pkl","rb")
fpn = open(r"F:\research\Graduation\GetData_createGraph\MoreData\orginfo.pkl","rb")
fp_third = open(r"F:\research\Graduation\GetData_createGraph\AnotherData\orginfoAnotherChina.pkl","rb")
fp_fourth = open(r"F:\research\Graduation\GetData_createGraph\FourthData\orginfoFourthData.pkl","rb")
ngo = pickle.load(fp)
ngoNew = pickle.load(fpn)
ngoThird = pickle.load(fp_third)
ngoFourth = pickle.load(fp_fourth)
print(len(ngo),len(ngoNew),len(ngoThird),len(ngoFourth))
cnt = 0
nameList = []

def mostSame(pat,searchSet,flag):
	l = len(searchSet)
	max = 0
	ans = None
	loc = 0
	for index in range(0,l):
		if flag:
			name = searchSet[index].name
		else:
			name = searchSet[index]
		simi = difflib.SequenceMatcher(None,pat,name).ratio()
		if simi > max:
			ans = searchSet[index]
			max = simi
			loc = index
	return max,ans,loc
flag = True
print("merging org and second Data:") #merge loc,time and scale,connectionInfo
for perNgo in ngo:
	if perNgo.location.find("拖动") != -1:
		perNgo.location = ""
	[max,perNgoNew,index] = mostSame(perNgo.name,ngoNew,flag)
	if max > 0.85:
		# print("name:",perNgo.name, "loc: ",perNgo.location,"newName:",perNgoNew.name)
		loc = perNgo.location.strip()
		if perNgo.location.strip() == "":
			perNgo.location = perNgoNew.location
		if perNgo.esTime == 0:
			perNgo.esTime = perNgoNew.esTime
		if perNgo.scale == "" or perNgo.scale == None and perNgoNew.scale != None:
			perNgo.scale = perNgoNew.scale
		if perNgo.connectionInfo == "":
			for i in range(0,len(perNgoNew.connectionInfo)):
				perNgo.connectionInfo += perNgoNew.connectionInfo[i]
		cnt = cnt + 1

temNgo = []
print("merge fourth data with third to become new fourth:") #merge loc,time,scale and sponsors
for perNgo in ngoFourth:
	[max,perNgoNew,index] = mostSame(perNgo.name,ngoThird,flag)
	if max > 0.85:
		perNgo.location = perNgoNew.location
		if perNgo.esTime == 0:
			perNgo.esTime = perNgoNew.esTime
		perNgo.scale = perNgoNew.scale
		perNgo.sponsors = perNgoNew.sponsors
		if perNgo.partners == []:
			perNgo.partners = perNgoNew.partners

print("merging org and FourthData Data: ") # merge time,field,descri and partners
for perNgoNew in ngoFourth:
	[max,perNgo,index] = mostSame(perNgoNew.name,ngo,flag)
	if max > 0.8:
		print(perNgo.name,perNgoNew.name)
		if perNgoNew.esTime != 0:
			ngo[index].esTime = perNgoNew.esTime
		ngo[index].partners = perNgoNew.partners
	else:
		ngo.append(perNgoNew)   #add data from fourth

print("merging org and third Data: ") #merge loation , esTime,scale and partners,sponors
for perNgoNew in ngoThird:
	[max,perNgo,index] = mostSame(perNgoNew.name,ngo,flag)
	if max > 0.8:
		# print(perNgo.name,perNgoNew.name,perNgoNew.partners)
		if perNgoNew.location != "" and  perNgo.location == "":
			ngo[index].location = perNgoNew.location
		if perNgoNew.esTime != 0:
			ngo[index].esTime = perNgoNew.esTime
		if perNgo.scale == "":
			ngo[index].scale = perNgoNew.scale
		if perNgoNew.partners != [] and perNgo.partners == []:
			ngo[index].partners = perNgoNew.partners
		if perNgoNew.sponsors != []:
			ngo[index].sponsors = perNgoNew.sponsors
print("endMerge")

for per in ngo:
	nameList.append(per.name)
flag = False

print("change name in partners and sponsors:")
for perNgo in ngo:
	tem = perNgo.partners
	for i in range(0,len(tem)):
		partner = tem[i]
		[max,name,index] = mostSame(partner,nameList,flag)
		# print(perNgo.name,partner,name,max)
		if max > 0.85:
			print(partner,name)
			perNgo.partners[i] = name
	# print(intem)

for perNgo in ngo:
	tem = perNgo.sponsors
	for i in range(0,len(perNgo.sponsors)):
		sponsor = perNgo.sponsors[i]
		[max,name,index] = mostSame(sponsor,nameList,flag)
		# print(perNgo.name,name)
		if max > 0.85:
			print(sponsor,name)
			perNgo.sponsors[i] = name

print("cnt: ",cnt)
print("writing to orginfoFinal.pkl")
with open("orginfoFinal.pkl","wb") as fp:
	pickle.dump(ngo,fp)
fp.close()
print("succ!")