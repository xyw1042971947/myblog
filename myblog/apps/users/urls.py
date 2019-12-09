from django.conf.urls import url

from .views import UserProfileView, change_profile_view, UserUpdateProfileView

appname = 'users'

urlpatterns = [
    url(r'^profile/$', UserProfileView.as_view(), name='profile'),
    url(r'^profile/change/$', UserUpdateProfileView.as_view(), name='profile_change'),
]
