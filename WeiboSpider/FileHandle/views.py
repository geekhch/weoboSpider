# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import xlrd


# 接受前端传来的文件
def upload_file(request):
    if request.method == "POST":
        print("post request")
        f = request.FILES['file']
        workbook = xlrd.open_workbook(filename=None, file_contents=f.read())
        worksheets = workbook.sheet_names()
        print('worksheets is %s' % worksheets)
        return HttpResponse("hhh")
    else:
        print("get request")
        return HttpResponse("please use GET method")
