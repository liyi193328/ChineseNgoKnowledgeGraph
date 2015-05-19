# import mysql.connector
# from mysql.connector import errorcode

# try:
#   cnx = mysql.connector.connect(user='root',port = '3307',database='test')
#   cursor = cnx.cursor();

#   cursor.execute("truncate user")
#   add = ("insert into user(name,password) values(%s,%s)")
#   data = ("mlx",1)
#   cursor.execute(add,data)
#   data = ("cwl",2)
#   cursor.execute(add,data)

#   # cursor.execute("select * from user")
#   cursor .execute("select * from user")
#   All = cursor.fetchall()
#   # print(All)
#   for x,y in All:
#     print(x,y)

#   cnx.commit()
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exists")
#   else:
#     print("erroro",err)
# else:
#   cnx.close()

# from bs4 import BeautifulSoup

# fp = open("30.html","r",encoding = "utf-8")
# soup = BeautifulSoup(fp.read())
# flag = list()
# x = soup.find_all('a',attrs={'name':'field_type'})
# for text in x:
#   flag.append(text.get_text())
# newf = list()
# for x in flag:
#   if x not in newf:
#     newf.append(x)
# print(newf)

# fieldName = ['全部', ' 劳工', '环保与动保', '三农/社区发展与救灾', '教育', '健康与防艾', 
#                 '性别与性少数', '老人与儿童', '残障', '社会创新/社会企业', 
#                 '能力建设/研究/支持/咨询', '民族/宗教/文化/艺术', 
#                 '企业社会责任', '社工', '其他']

# from bs4 import BeautifulSoup
# from getInfo import getInfo
# url = "http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type=0&field_type=0&area_type=1&province_type=1&city_type=0&market_type=0&keywords="

# html = getInfo(url)
# soup = BeautifulSoup(html)

# ele = soup.find("dd","sel_b").find_all("a")
# y = []
# for x in ele:
#   y.append(x.get_text())
# print(y)

import pickle,re
# ngo = list()

# for i in range(10,12):
#   filename = "orginfo"+str(i)+".pkl"
#   with open(filename,"rb") as fp:
#       ngo0 = pickle.load(fp)
#       for perngox in ngo0:
#           ngo.append(perngox)
#           # print(perngox.name)
# newNgo = list()
# for i in range(0,len(ngo)):
#   if(ngo[i].name != ""):
#     flag = False
#     for j in range(i+1,len(ngo)):
#       if(ngo[i].name == ngo[j].name):
#         flag = True
#         break
#     if flag == False:
#         newNgo.append(ngo[i])
# print("ngo Itemm: %d"%len(newNgo))
# print("writing to orginfo_new.pkl!")
# with open("orginfo_new.pkl","wb") as fp:
#   pickle.dump(newNgo,fp)
# print("succ!")

from getInfo import getInfo
from bs4 import BeautifulSoup
# html = getInfo("http://www.chinadevelopmentbrief.org.cn/service/action/org_search.php?org_type=0&field_type=0&area_type=1&province_type=0&city_type=0&market_type=0&keywords=")
# soup = BeautifulSoup(html)
# # print(html)
# pat = re.compile(r'org_type=0&field_type=0&area_type=1&province_type=(\d+)')
# num = re.findall(pat,html)
# print(num)
import os


