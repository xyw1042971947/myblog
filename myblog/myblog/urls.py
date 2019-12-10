"""myblog URL Configuration

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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from apps.users.views import loginView, LogoutView
from apps.blog.views import IndexView, ArchiveListView, Ceshi
from blog.feeds import AllArticleRssFeed
import xadmin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url('', include('blog.urls', namespace='blog')),
    url(r'^comment/', include('comment.urls', namespace='comment')),#评论
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('users.urls', namespace='users')),#账户

    url(r'archive/', ArchiveListView.as_view(), name='archive'), #归档
    url(r'^feed/$', AllArticleRssFeed(), name='rss'),   # rss订阅
    url(r'^ceshi/$', Ceshi.as_view(), name='ceshi'),   # 测试
    url(r'login/', loginView.as_view(), name='login'),
    url(r'logout/', LogoutView.as_view(), name='logout'),
    url(r'hot/',IndexView.as_view(), {"sort": "V"}, name='hot')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
