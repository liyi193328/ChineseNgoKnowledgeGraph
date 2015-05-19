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


# import pickle

# fp = open("orginfo.pkl","rb")
# ngo = list()
# while True:
# 	try:
# 		tem = pickle.load(fp)
# 		for i in tem:
# 			print(i.name)
# 			ngo.append(i)
# 		# ngo.append(i for i in pickle.load(fp))
# 	except EOFError:
# 		break
# with open("orginfo_merge.pkl","wb") as fp:
# 	pickle.dump(ngo,fp)
# print("succ")

# import os,sys
# print(os.getcwd())
# print(os.path.dirname(os.getcwd()))
import pickle
with open("orginfoAnotherChina.pkl","rb") as fp:
	ngo = pickle.load(fp)
	for per in ngo:
		print(per.name,per.url+"\n",per.partners)