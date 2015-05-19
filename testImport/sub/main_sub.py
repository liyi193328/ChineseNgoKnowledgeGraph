import os,sys,pprint
sys.path.append(os.path.dirname(os.getcwd())) #我将父文件目录导入到系统运行目录中，然后就可以导入父亲目录下的模块了
pprint.pprint(sys.path)
# import testImport
# import testImport.a
from a import a
print(a())