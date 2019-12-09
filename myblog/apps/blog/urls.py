from django.conf.urls import url

from .views import IndexView, CategoryListView, ArticleDetailView, TagListView

appname = 'blog'

urlpatterns = [
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^article/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='detail'),  # 文章内容页
    url(r'^tag/(?P<slug>[\w-]+)/$', TagListView.as_view(), name='tag'),  # 标签
    url(r'^tag/(?P<slug>[\w-]+)/hot/$', TagListView.as_view(), {'sort': 'V'}, name='tag_hot'),  # 标签
    url(r'^category/(?P<slug>[\w-]+)/$', CategoryListView.as_view(), name='category'), 
    url(r'^category/(?P<slug>[\w-]+)/hot/$', CategoryListView.as_view(), {'sort': 'V'},name='category_hot'),  
]
