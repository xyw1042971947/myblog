import xadmin
from xadmin import views

from .models import Keyword, Tag, Category, Article, Timeline, Carousel, Silian, FriendLink


class ArticleAdmin(object):
    data_hierarchy = 'create_data'

    #如果设置了这个属性，它表示应该从表单中去掉的字段列表。
    exclude = ('views', )

     # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'title', 'author', 'create_date', 'update_date')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('create_date', 'category')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    filter_horizontal = ('tags', 'keywords')  # 给多选增加一个左右添加的框

    def get_queryset(self, request):
        qs = super(Article, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
        
class CategoryAdmin(object):
    list_display = ('name', 'id', 'slug')

class TagAdmin(object):
    list_display = ('name', 'id', 'slug')

class TimelineAdmin(object):
    list_display = ('title', 'side', 'update_date', 'icon', 'icon_color',)

    #设置fieldsets 控制管理“添加”和 “更改” 页面的布局.
    fieldsets = (
        ('图标信息', {'fields': (('icon', 'icon_color'),)}),
        ('时间位置', {'fields': (('side', 'update_date', 'star_num'),)}),
        ('主要内容', {'fields': ('title', 'content')}),
    )
    date_hierarchy = 'update_date'
    list_filter = ('star_num', 'update_date')

class CarouselAdmin(object):
    list_display = ('number', 'title', 'content', 'img_url', 'url')

class SilianAdmin(object):
    list_display = ('id', 'remark', 'badurl', 'add_date')

class KeywordAdmin(object):
    list_display = ('name', 'id')

class FriendLinkAdmin(object):
    list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
    date_hierarchy = 'create_date'
    list_filter = ('is_active', 'is_show')

xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Keyword, KeywordAdmin)
xadmin.site.register(Timeline, TimelineAdmin)
xadmin.site.register(Carousel, CarouselAdmin)
xadmin.site.register(Silian, SilianAdmin)
xadmin.site.register(FriendLink, FriendLinkAdmin)