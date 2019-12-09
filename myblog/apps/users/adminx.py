import xadmin
from xadmin import views

from .models import VerifyCode


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = False

class GlobalSettings(object):
    site_title = "我的博客"
    site_footer = "后台管理系统"
    # menu_style = "accordion"

class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)