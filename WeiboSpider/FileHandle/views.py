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
        table = workbook.sheet_by_index(0)  # 取第一张工作簿
        print(table.cell(0,0).value)
        return HttpResponse("hhh")
    else:
        print("get request")
        return render(request, 'index.html')
