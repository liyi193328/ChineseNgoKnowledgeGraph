import os
# os.system("python getOrgNumber.py")#获取组织的的site编号
# os.system("python main.py")   #获取ngo发展网中每一个组织的初略信息
# os.system("python getProvince.py")  #从ngo发展网中获取组织的省份（1005个），部分不全
# os.system("python getOrgType.py")  #得到机构类型
os.system("python mergeData.py")  #合并公益项目2.0的结构信息，根据同名字信息合并的原则
os.system("python addData.py")  #没有地址的，从文本中解析机构的地址名字，根据地址获取改地址的省份
# os.system("python createGraph.py")  #创建图
