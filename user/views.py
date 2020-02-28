from django.shortcuts import redirect
import hashlib
import random
import string
import time
from datetime import datetime
from django.core.mail import send_mail
from . import models


def login(func):   # 登陆认证修饰器
    def wrapper(*args, **kwargs):
        request = args[0]
        user = request.COOKIES.get('username', None)
        info = models.UserInfo.objects.filter(username=user)
        if not info.exists():
            return redirect("login")    # 没有找到用户信息则跳转认证
        if info[0].auth:   # 认证标志位为认证过
            date = datetime.strptime(info[0].login_time, '%Y-%m-%d %H:%M:%S')
            if (datetime.now() - date).seconds > 3600:  # session失效
                info.update(auth=0)
                rd = redirect("login")  # 清除cookie
                rd.delete_cookie("username")
                return rd
            else:
                return func(*args, **kwargs)
        else:
            return redirect("login")
    return wrapper


def is_authed(request):
    username = request.COOKIES.get("username", None)
    if username and models.UserInfo.objects.get(username__exact=username).auth:
        return True
    else:
        return False


def auth(request):  # 检测用户名和密码
    username = request.POST.get('username', None)
    password = request.POST.get("password", None)
    if models.UserInfo.objects.filter(username__exact=username, password__exact=password).exists():
        if models.UserInfo.objects.filter(username__exact=username, password__exact=password).update(auth=1, login_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())):
            return True
    return False


def logout(request):    # 注销登陆
    username = request.COOKIES.get('username', None)
    if models.UserInfo.objects.filter(username__exact=username).update(auth=0, login_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())):
        return True
    else:
        return False


def email_resend(request):
    email = request.POST.get('email', None)
    verification = ''.join(random.sample(string.ascii_letters + string.digits, 6))  # 生成随机验证码
    subject = "邮箱验证"
    message = "来自航空系统的邮箱验证码为：" + verification + ", 五分钟内有效，若非本人操作，请不予理睬"
    if send_mail(subject, message, '13296692963@163.com', ['1043213248@qq.com', email]):
        if models.TmpUserInfo.objects.filter(email=email).update(verification_code=hashlib.md5(email + verification).hexdigest()):
            return True
    else:
        return False  # 发送验证码失败


def register_auth(request):
    email = request.POST.get('email', None)
    verification = request.POST.get('verification', None)   # 检测验证码和邮箱是否绑定成功
    m = hashlib.md5()
    m.update((email + verification).encode("utf-8"))
    search_info = models.TmpUserInfo.objects.filter(email=email, verification_code=m.hexdigest())
    if search_info.exists():    # 如果查到记录存在，包括邮箱相同的记录
        register_user = search_info.filter(email=email, verification_code=m.hexdigest())[0]     # 提出注册验证成功用户
        if models.UserInfo.objects.create(username=register_user.username, password=register_user.password, email=email, phone=register_user.phone):
            models.TmpUserInfo.objects.filter(verification_code=m.hexdigest()).delete()
            return True
    else:
        return False


def register(request):  # 用户注册逻辑
    user = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    if models.UserInfo.objects.filter(username=user).exists():
        return 2    # 用户名存在返回代码2
    if models.UserInfo.objects.filter(email=email).exists():
        return 3    # 邮箱重复
    try:
        verification = ''.join(random.sample(string.ascii_letters + string.digits, 6))  # 生成随机验证码
        subject = "邮箱验证"
        message = "来自航空系统的邮箱验证码为：" + verification + ", 五分钟内有效，若非本人操作，请不予理睬"
        if send_mail(subject, message, '13296692963@163.com', [email]):
            m = hashlib.md5()
            m.update(email.encode('utf-8') + verification.encode('utf-8'))
            if models.TmpUserInfo.objects.filter(email=email).exists():     # 邮箱重复则更新
                models.TmpUserInfo.objects.filter(email=email).update(username=user, password=password, phone=phone, email=email, verification_code=m.hexdigest())
                return 1
            else:   # 不存在则新建
                models.TmpUserInfo.objects.create(username=user, password=password, phone=phone, email=email, verification_code=m.hexdigest())
                return 1
        else:
            return 4    # 发送验证码失败
    except:
        return 0
