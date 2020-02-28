from django.db import models

# Create your models here


class UserInfo(models.Model):
    username = models.CharField("用户名", max_length=10, null=False)
    password = models.CharField("密码", max_length=20, null=False)
    login_time = models.CharField("登陆时间", max_length=20, null=True)
    auth = models.SmallIntegerField("认证状态", default=0)


class TmpUserInfo(models.Model):
    username = models.CharField("用户名", max_length=255, null=False)
    password = models.CharField("密码", max_length=20, null=False)
    email = models.EmailField("邮箱", null=False)
    phone = models.CharField("电话", max_length=11, null=False)
    verification_code = models.CharField("验证码", max_length=32, null=False)
