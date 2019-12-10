import time, datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings
from django.utils.text import slugify
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet
from django.core.cache import cache

from markdown.extensions.toc import TocExtension
import markdown

from blog.models import Article, Category, Tag
# Create your views here.


class Ceshi(generic.TemplateView):
    template_name = '404.html'

class IndexView(generic.ListView):
    '''
        首页文章列表
    '''
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 0

    def get_ordering(self):
        ordering = super(IndexView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == "V":
            return ('-views', '-update_date', '-id')
        return ordering


class ArticleDetailView(generic.DetailView):
    """
        文章详情页面
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        """
            返回该视图要显示的对象。 如果提供了queryset，该查询将被用作对象的源；否则将使用get_queryset()。
            get_object()在视图的参数中查找一个pk_url_kwarg参数；如果找到此参数，此方法将使用该值执行基于主键的查找。 
            如果这个参数没有找到，该方法查找slug_url_kwarg参数，使用slug_field字段执行针对slug的查询。
        """
        obj = super(ArticleDetailView, self).get_object()
        user = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if user != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()

        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            md = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            cache.set(md_key, md, 60 * 60 * 12)
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj


class CategoryListView(generic.ListView):
    """
        分类文章列表
    """
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 0

    def get_ordering(self):
        ordering = super(CategoryListView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == "V":
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryListView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self):
        context_data = super(CategoryListView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate

        return context_data

class TagListView(generic.ListView):
    model = Article
    template_name = 'blog/tag1.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 0

    def get_ordering(self):
        ordering = super(TagListView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'V':
            return ('-views', '-update_date', '-id')
        return ordering
    
    def get_queryset(self, **kwargs):
        queryset = super(TagListView, self).get_queryset()
        cate = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=cate)

    def get_context_data(self):
        context_data = super(TagListView, self).get_context_data()
        cate = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = cate

        return context_data

class ArchiveListView(generic.ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'
    paginate_by = 200
    paginate_orphans = 50    


#重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    context_object_name = 'search_list'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views')
