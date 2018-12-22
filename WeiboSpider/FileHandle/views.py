# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Spider.analysis.dataView import DataView
from Spider.utils import *
import re
import xlrd

xls_gener = DataView()

success_response = {'dataStatus': "1"}
empty_uid_response = {'dataStatus': "2"}
empty_email_response = {'dataStatus': "3"}
error_email_response = {'dataStatus': "4"}

# 接受前端传来的文件
@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        f = request.FILES['file']
        workbook = xlrd.open_workbook(filename=None, file_contents=f.read())
        table = workbook.sheet_by_index(0)  # 取第一张工作簿
        functionName = table.cell(1, 1).value
        receiver_email = str(table.cell(3, 1).value)
        if functionName == 'UserIndexInfo':
            if table.cell(2,1).value is '':
                return JsonResponse(empty_uid_response)
            elif receiver_email is '':
                return JsonResponse(empty_email_response)
            elif not validate_email(receiver_email):
                return JsonResponse(error_email_response)
            else:
                path = xls_gener.blogs_to_xls(int(table.cell(2, 1).value))
                MAIL('博主所有微博内容', receiver_email, path)
                return JsonResponse(success_response)
        elif functionName == 'UserBaseInfo':
            uids = []
            rows = table.row_values(2)  # 获取第3行的所有值
            for r in rows[1:]:
                uids.append(int(r))
            print(uids)
            if uids is '':
                return JsonResponse(empty_uid_response)
            elif receiver_email is '':
                return JsonResponse(empty_email_response)
            elif not validate_email(receiver_email):
                return JsonResponse(error_email_response)
            else:
                path = xls_gener.profile_to_xls(uids)
                MAIL('根据uid生成用户基本信息', receiver_email, path)
                return JsonResponse(success_response)
        elif functionName == 'UserWorldCloud':
            if table.cell(2,1).value is '':
                return JsonResponse(empty_uid_response)
            elif receiver_email is '':
                return JsonResponse(empty_email_response)
            elif not validate_email(receiver_email):
                return JsonResponse(error_email_response)
            else:
                path = xls_gener.word_cloud(int(table.cell(2, 1).value))
                MAIL('生成用户词云', receiver_email, path)
                return JsonResponse(success_response)
        elif functionName == 'FansInfo':
            if table.cell(2,1).value is '':
                return JsonResponse(empty_uid_response)
            elif receiver_email is '':
                return JsonResponse(empty_email_response)
            elif not validate_email(receiver_email):
                return JsonResponse(error_email_response)
            else:
                path = xls_gener.fans_profile_to_xls(int(table.cell(2, 1).value))
                MAIL('根据uid生成粉丝信息', receiver_email, path)
                return JsonResponse(success_response)
        elif functionName == 'FansFollowingInfo':
            if table.cell(2,1).value is '':
                return JsonResponse(empty_uid_response)
            elif receiver_email is '':
                return JsonResponse(empty_email_response)
            elif not validate_email(receiver_email):
                return JsonResponse(error_email_response)
            else:
                path = xls_gener.folows_profile_to_xls(int(table.cell(2, 1).value))
                MAIL('根据uid生成关注用户信息', receiver_email, path)
                return JsonResponse(success_response)
        elif functionName == 'UserDetailInfo':
            pass
    else:
        print("get request")
        return HttpResponse("请使用POST方法")


# 邮箱格式判定
def validate_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        return False


