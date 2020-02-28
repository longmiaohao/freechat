from django.shortcuts import render, redirect
from django.http import JsonResponse
from user import views as user_views
from RawSql import *
import json


def login(request):
    if user_views.is_authed(request):
        return redirect("index")
    if request.method == "POST":
        if user_views.auth(request):
            rd = redirect('index')
            rd.set_cookie("username", request.POST.get("username"))
            return rd
        else:
            error_message = "密码或者用户名错误"
            username = request.POST.get("username")
            return render(request, "login/login.html", locals())
    else:
        return render(request, "login/login.html", locals())


@user_views.login
def index(request):
    username = request.COOKIES["username"]
    return render(request, "index/index.html", locals())


def logout(request):
    user_views.logout(request)
    rd = redirect("login")
    rd.delete_cookie('username')
    return rd


# def email(request):
#     from django.core.mail import send_mail
#     from team import settings
#     if request.method == "POST":
#         emails = ['951479374@qq.com','1043213248@qq.com', '893830907@qq.com', 'lmmaturezhang@163.com', '786986140@qq.com', '1318867480@qq.com']
#         message = request.POST.get("message")
#         xm = request.POST.get("xm")
#         njzy = request.POST.get("njzy")
#         email = request.POST.get("email")
#         try:
#             message = "发送者邮箱：" + email + "\n姓名:" + xm + "\n年级专业:" + njzy + '\n' + message + "\n"
#             if send_mail("双零团队2019秋季招新", message, settings.EMAIL_HOST_USER, emails, fail_silently=True):
#                 message = "已经收到你的来信，期待你的加入"
#                 return JsonResponse({"msg": message, "code": "01"}, safe=False, status=200)
#         except:
#             message = "分享失败，邮件发送出现异常"
#             return JsonResponse({"msg": message, "code": "00"}, safe=False, status=405)
#     return redirect("home")


@user_views.login
def chat(request):
    username = request.GET.get("username")
    table_name = request.COOKIES["username"]
    sql = "select cast(time as char) time, type, username, content from %s where username='%s'  order by time desc limit 10" % (table_name, username)
    rawsql = RawSql()
    data = rawsql.get_json(sql)
    if data:
        data = json.loads(data.replace('None', '""'))
        for var in data:
            var['content'] = base64.b64decode(str.encode(var['content']))
        data = reversed(data)
    return render(request, "chat/chat.html", locals())


def contact(request):
    rawsql = RawSql()
    sql = "select username, auth status, login_time status_time from user_userinfo  where username != '%s' order by auth desc" % request.GET.get("username")
    data = rawsql.get_json(sql)
    return JsonResponse(json.loads(data.replace('None', '""')), safe=False)


def ws(request):
    return JsonResponse({"status": "ok"}, safe=False)


def page_not_found(request, exception):
    return render(request, 'errors/404.html')
