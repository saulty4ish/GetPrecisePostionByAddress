#!/usr/bin/env python
# -*- coding:utf-8
import requests
import csv
import json
api="https://maps.googleapis.com/maps/api/geocode/json?address=" #api地址
key="AIzaSyCPLRDsRhNZ1HRw_S9L5G2QxoHb0hQl-sI"  #Goole提供的apikey，谷歌用户免费获取
headers = {'Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
filename="Address.csv"                       #存放地址文件路径
proxies={"https":"https://127.0.0.1:1080"}    #设置代理，我这里采用ssr翻墙
result="result.txt"                   #以txt格式输出

def GetNameOfPlace(filename):         #从csv文件读取地址放入dict
	Targets=[]
	with open(filename,"r") as f:
		r = csv.DictReader(f)
		for line in r:
			Targets.append(line['Location'])
	return Targets
def AnalysisJson(response,Target):       #解析api返回的json数据
	json_string=json.dumps(response)
	responseJson=json.loads(json_string)
	lat = responseJson.get('results')[0]['geometry']['location']['lat']
	lng = responseJson.get('results')[0]['geometry']['location']['lng']
	print("[+] The Location of %s is : %f, %f"%(Target,lat, lng))
	ret=str(lat)+","+str(lng)
	return ret

def Output(ret):                 #结果输出到本地文件
	with open("result.txt","a") as f:
		f.write(ret+"\n")
		
def VisitWithProxy(Targets,proxies):   #构造url,Get方式访问api获取数据
	for Target in Targets:
		payload=api+str(Target.strip())+"&key="+key
		try:
			r=requests.get(payload,proxies=proxies,timeout=10)
		except:
			print "[-] Somthing wrong with server..."
		try:
			ret=AnalysisJson(r.json(),Target)
			Output("("+ret+")")
		except:
			print "[-] no result of %s"%(Target)
			Output("Wrong,Please check it .")
Targets=GetNameOfPlace(filename)
VisitWithProxy(Targets,proxies)