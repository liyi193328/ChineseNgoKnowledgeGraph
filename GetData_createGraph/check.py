import orgClass
import getInfo
import os
import time
import re

s1 = r'<div class="ml_name mt15">'
s2_1 = r'<h1>'
s2_2 = r'</h1>'
s3_1 = r'<font>'
s3_2 = r'</font>'
name = enName = esTime = location = area = scale = description = info = recruit = image = None

fp = open("Pages.txt", "r", encoding="utf-8")  # os.system("pause")
# time.sleep(2)
# url = st.strip()
html = getInfo.getInfo('http://www.chinadevelopmentbrief.org.cn/org33/')
loc = html.find(s1)
if loc != -1:
    x = html.find(s2_1, loc + len(s1))
    if x == -1:pass
    y = html.find(s2_2, x + len(s2_1))
    if y == -1:pass
    name = html[x + len(s2_1):y]
    print(name)
    m = html.find(s3_1, y + len(s2_2))
    if m == -1:pass
    n = html.find(s3_2, m + len(s3_1))
    if(n == -1):pass
    enName = html[m + len(s3_1):n]
    print(enName)
    Gr = re.search(r'<li><font>成立时间：</font>(\d+)年</li>', html[n:])
    esTime = int(Gr.group(1))
    print(esTime)

    Gr = re.search(r'<li><font>机构规模：\s{0,10}</font>(.*)</li>',html) 
    scale = Gr.group(0)
    print(scale)
