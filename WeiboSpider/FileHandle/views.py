# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Spider.analysis.dataView import DataView
from Spider.utils import *
import xlrd

xls_gener = DataView()

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
        if functionName == 'UserIndexInfo':
            path = xls_gener.blogs_to_xls(int(table.cell(2, 1).value))
            MAIL('博主所有微博内容', table.cell(3, 1), path)
        elif functionName == 'UserBaseInfo':
            uids = []
            rows = table.row_values(2) # 获取第3行的所有值
            for r in rows[1:]:
                uids.append(int(r))
            path = xls_gener.profile_to_xls(uids)
            MAIL('根据uid生成用户基本信息', table.cell(3, 1), path)
        elif functionName == 'UserWorldCloud':
            path = xls_gener.blogs_to_xls(int(table.cell(2, 1).value))
            MAIL('生成用户词云', table.cell(3, 1), path)
        elif functionName == 'FansInfo':
            path = xls_gener.blogs_to_xls(int(table.cell(2, 1).value))
            MAIL('根据uid生成粉丝信息', table.cell(3, 1), path)
        elif functionName == 'FansFollowingInfo':
            path = xls_gener.blogs_to_xls(int(table.cell(2, 1).value))
            MAIL('根据uid生成关注用户信息', table.cell(3, 1), path)
        elif functionName == 'UserDetailInfo':
            pass
        response = {
            'dataStatus': "1"
        }
        return JsonResponse(response)
    else:
        print("get request")
        return HttpResponse("请使用POST方法")
