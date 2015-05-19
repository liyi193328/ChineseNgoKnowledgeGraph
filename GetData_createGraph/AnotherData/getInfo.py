import urllib.request,urllib.error
import time
import string
import re
import urllib
import urllib.request
import chardet
import os

def getInfo(url):
	while True:
		try:
			# print("getting html...")
			html = urllib.request.urlopen(url).read()
			html = html.decode("utf-8")
			return html
		except urllib.error.URLError as e:
			print(e)
			# raise
		except:
			raise

# html = getInfo(r'http://www.chinadevelopmentbrief.org.cn/org33/') 
# print(html)