import pprint,codecs,json

fp = codecs.open("dataSearch.json","r","utf-8")
data = fp.read()
# jsonD = json.loads(data,encoding="utf-8")
pprint.pprint(data)