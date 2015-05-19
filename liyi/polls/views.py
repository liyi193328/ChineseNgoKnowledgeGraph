from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from polls.models import mainHandle,updateData,getProvinceTime,getNode
import logging
import json
# Create your views here.

def about(req):
    return render_to_response("about.html")

def index(req):
    return render_to_response("index.html")

def search(req):
    return render_to_response("search.html")

def searchProvinceTime(req):
    if req.is_ajax and req.method == "POST":
        body = req.body.decode("utf-8")
        requestBody = json.loads(body)
        ngoList = getProvinceTime(requestBody['province'],requestBody['time'])
        return JsonResponse( {"ngoList":ngoList} )

def searchSingle(req):
    if req.is_ajax and req.method == "POST":
        body = req.body.decode("utf-8")
        requestBody = json.loads(body)
        perNgo = getNode(requestBody['nodeID'])
        return JsonResponse(perNgo)

def extendNode(req):
    if req.is_ajax and req.method == 'POST':
        body = req.body.decode("utf-8")
        requestBody = json.loads(body)
        fp=open("request_body.json","w+",encoding = "utf-8")
        fp.write(str(requestBody))
        dataSet = requestBody['dataSet']
        updateNodeID = requestBody['updateNodeID']
        id = requestBody['id']
        newData = updateData(dataSet,updateNodeID,id)
        fp = open("data_ExNode.json","w+")
        fp.write(json.dumps(newData)) 
        # newData = dataSet
        return JsonResponse(newData)

def getSearchData(req):
    if req.is_ajax:
        searchInfo = {'orgType': "", 'field': "", 'province': "", "nameA": "","nameB":""}
        if 'orgType' in req.GET:
            searchInfo['orgType'] = req.GET['orgType']
        if 'field' in req.GET:
            searchInfo['field'] = req.GET['field']
        if 'province' in req.GET:
            searchInfo['province'] = req.GET['province']
        if 'nameA'in req.GET:
            searchInfo['nameA'] = req.GET['nameA']
        if 'nameB' in req.GET:
            searchInfo['nameB'] = req.GET['nameB']
        data = mainHandle(searchInfo)
        # fp = open("data.json","w+")
        # fp.write(json.dumps(data)) 
        return JsonResponse(data)
