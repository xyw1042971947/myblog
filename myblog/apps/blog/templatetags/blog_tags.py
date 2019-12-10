from django import template
from django.db.models.aggregates import Count

from blog.models import Carousel, Category, Tag, FriendLink


register = template.Library()

@register.simple_tag
def get_carousel_index():
    '''返回幻灯片列表'''
    return Carousel.objects.filter(number__lte=5)

@register.simple_tag
def get_category_list():
    '''返回分类列表'''
    return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

@register.simple_tag
def get_tag_list():
    '''返回标签列表'''
    return Tag.objects.annotate(total_num=Count('article'))

@register.simple_tag
def get_friendlink_list():
    '''返回友情链接列表'''
    return FriendLink.objects.filter(is_active=True).filter(is_show=True)

@register.simple_tag
def my_highlight(text, q):
    '''自定义标题搜索词高亮函数，忽略大小写'''
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text
