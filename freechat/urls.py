"""freechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler404
from index import views as index_views

urlpatterns = [
    url(r'^login$', index_views.login, name='login'),
    url(r'^logout$', index_views.logout, name='logout'),
    url(r'^chat$', index_views.chat, name='chat'),
    url(r'^contact$', index_views.contact, name='contact'),
    url(r'ws', index_views.ws, name='ws'),
    url(r'', index_views.index, name='index'),
]

# handler404 = index_views.page_not_found
