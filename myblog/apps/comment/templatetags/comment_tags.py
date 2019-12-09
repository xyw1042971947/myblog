from django import template
from django.db.models.aggregates import Count

from comment.models import ArticleComment


register = template.Library()

@register.simple_tag
def get_comment_count(entry):
    """
        返回评论列表
    """
    lis = entry.article_comments.all()
    return lis.count()

@register.simple_tag
def get_comment_user_count(entry):
    """
        返回参与评论人数
    """
    p = []
    lis = entry.article_comments.all()
    for each in lis:
        if each.author not in p:
            p.append(each.author)
    return len(p)

@register.simple_tag
def get_parent_comments(entry):
    """
        返回父级评论列表
    """
    lis = entry.article_comments.filter(parent=None)
    return lis

@register.simple_tag
def get_child_comments(entry):
    """
        返回子级评论列表
    """
    lis = entry.articlecomment_child_comments.all()
    return lis

@register.simple_tag
def get_notifications(user, f=None):
    if f=="true":
        lis = user.notification_get.filter(is_read=True)
    elif f=="false":
        lis = user.notification_get.filter(is_read=False)
    else:
        lis = user.notification_get.all()
    return lis

@register.simple_tag
def get_notifications_count(user,f=None):
    '''获取一个用户的对应条件下的提示信息总数'''
    if f=='true':
        lis = user.notification_get.filter(is_read=True)
    elif f=='false':
        lis = user.notification_get.filter(is_read=False)
    else:
        lis = user.notification_get.all()
    return lis.count()

@register.simple_tag
def get_notifications_count(user,f=None):
    '''获取一个用户的对应条件下的提示信息总数'''
    if f=='true':
        lis = user.notification_get.filter(is_read=True)
    elif f=='false':
        lis = user.notification_get.filter(is_read=False)
    else:
        lis = user.notification_get.all()
    return lis.count()