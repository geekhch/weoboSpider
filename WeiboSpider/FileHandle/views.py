# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from WeiboSpider.Spider.analysis import dataView
from WeiboSpider.Spider.utils import *
import xlrd

xls_gener = dataView()

# 接受前端传来的文件
@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        print("post request")
        f = request.FILES['file']
        workbook = xlrd.open_workbook(filename=None, file_contents=f.read())
        table = workbook.sheet_by_index(0)  # 取第一张工作簿
        print(table.cell(1, 1).value)
        functionName = table.cell(1, 1).value
        if(functionName == 'UserIndexInfo'):
            path = xls_gener.blogs_to_xls(table.cell(2, 1))
            MAIL('微博博主主页内容', table.cell(3, 1), path)
        response = {
            'dataStatus': "1"
        }
        return JsonResponse(response)
    else:
        print("get request")
        return HttpResponse("请使用POST方法")
