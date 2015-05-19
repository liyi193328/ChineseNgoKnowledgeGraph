from getOrgNumber import getOrgNumber
import pickle,os,re

urlPagef = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type=0&field_type=0&area_type=1&province_type="
urlPageS = "&market_type=0&keywords=&page="
# urlPagef = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type=0\
# &field_type=0&area_type=1&province_type="
# urlPageS = "&market_type=0&keywords=&org_search=&page="
prefix = r'http://www.chinadevelopmentbrief.org.cn/org'
seq = ['0','1', '2', '3', '4', '5', '7', '6', '9', '14', '12', '13', '11', '10', '22', '8', '23', '15', '17', '16', '20', 
'21', '32', '24', '25', '26', '33', '18', '19', '31', '30', '34', '43', '42', '44']

province = ['全部', '北京', '上海', '天津', '重庆', '黑龙江', '吉林', '辽宁', '内蒙古', 
			'新疆', '甘肃', '宁夏', '山西', '陕西', '河南', '河北', '山东', '西藏', '四川', 
			'青海', '湖南', '湖北', '江西', '安徽', '江苏', '浙江', '福建', '云南', '贵州', 
			'广西', '广东', '海南', '香港特别行政区', '台湾', '澳门特别行政区']
			
fp = open("orginfo_new.pkl","rb")
ngo = pickle.load(fp)
print("len(ngo): %d" %len(ngo))

fileSiteList = "province"
cnt = 0
Pages = 0
orgNum = set()
for i in range(1,len(province)):
	print(province[i])
	url = urlPagef + str(seq[i]) +  urlPageS
	(orgNumTem,pages) = getOrgNumber(url,prefix,fileSiteList)
	Pages = Pages + pages
	for per in orgNumTem:
		orgNum.add((per,i))
print("size_orgNum:",len(orgNum),Pages)

for perOrgNum in orgNum:
	for perNgo in ngo:
		if perNgo.orgNumber == perOrgNum[0]:
			perNgo.province = province[ perOrgNum[1] ] + "省"
			cnt = cnt + 1

print("cnt:",cnt)

for i in ngo:
    # print(i.connectionInfo)
    tem = list()
    # s = i.description.replace("\t", "").replace("\xa0","").replace("&nbsp;","").splitlines()
    # for j in range(0,len(s)):
    # 	if s[j] != "":
    # 		tem.append(s[j]+'\n')
    # # print(''.join(tem).splitlines())
    # # print(''.join(tem))
    # i.description = ''.join(tem)
    # st = i.description.strip()
    # xi = re.findall(r'&(.*);',st)
    # for j in xi:
    #     st = st.replace(j,"")
    # i.description = st
    # print(st)
    # input("x:")
    cnt = cnt + 1

    perNgo = i
    if perNgo.connectionInfo == []:
        perNgo.connectionInfo = ""

    con = "联系方式："
    st = perNgo.description
    findCon = st.find(con) #在介绍文字中查找联系方式
    if findCon != -1:
        perNgo.connectionInfo = st[findCon+len(con):len(st)]
        tem = "\n"
        #去掉开始的\n
        for per in  perNgo.connectionInfo.splitlines(True):
            if per != "\n":
                tem = tem + per
        perNgo.connectionInfo = tem
    i = perNgo

provinceNameMap = {"西藏省":"西藏自治区","内蒙省":"内蒙古自治区","广西省":"广西壮族自治区",
                    "新疆省":"新疆维吾尔自治区","宁夏省":"宁夏回族自治区"}
for i in ngo:
	if i.province:
        if i.province in provinceNameMap:
            i.province = provinceNameMap[i.province]
		elif re.search("北京|重庆|天津|上海",i.province):
			i.province = i.province.replace("省","市")
		elif re.search("香港特别行政区|台湾|澳门特别行政区",i.province):
			i.province = i.province.replace("省","")

print("writting to orginfo_add_province.pkl")
with open("orginfo_add_province.pkl","wb") as fp:
	pickle.dump(ngo,fp)
print("succ to write!")
fp.close()

