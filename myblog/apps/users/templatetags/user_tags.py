from django import template
from django.db.models.aggregates import Count

from comment.models import ArticleComment


register = template.Library()

@register.inclusion_tag('accounts/user_avatar.html')
def get_user_avatar_tag(user):
    """
        返回用户头像
    """
    return {'user': user}