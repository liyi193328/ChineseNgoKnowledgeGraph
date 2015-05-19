import urllib.request,urllib.parse
import json,pprint,time

def getAddFromBM(add):
	print("baiduAdd:",add)
	time.sleep(1.5)
	orData = {
			"address":add,
			"output":"json",
			"ak":"62a6776a6368a0c2d5e771ecf0025656"
			}
	Data = urllib.parse.urlencode(orData)
	req = urllib.request.Request("http://api.map.baidu.com/geocoder/v2/?%s"%Data)
	f = urllib.request.urlopen(req)
	s = json.loads(f.read().decode("utf-8"))
	print("get lat ,lng!")
	# print(s,type(s))
	if s.get('result') and s['result'] != []:
		loc = s['result']['location']
		lat = loc['lat']
		lng = loc['lng']
		req = urllib.request.Request("http://api.map.baidu.com/geocoder/v2/?ak=%s&location=%f,%f&output=json" %(orData['ak'],lat,lng))
		f = urllib.request.urlopen(req)
		js = f.read().decode("utf-8")
		s = json.loads(js)
		print("get location result!")
		# pprint.pprint(s)
		if s.get('result') and s['result'] != []:
			return s['result']['addressComponent']['province'],s['result']['formatted_address'],s
	return (-1,-1,s)

# print( getAddFromBM("北京市朝阳区黄渠东路2号院12号楼4单元502室（地铁六号线黄渠站A口出右转300米）") )





