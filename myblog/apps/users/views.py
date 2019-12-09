from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import LoginForm, ProfileForm
# Create your views here.

class loginView(View):
    """
        用户登录
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('blog:index'))
        return render(request, 'blog/login.html')
    
    def post(self, request, *args, **kwargs):  
        #表单验证
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                #查询到用户
                login(request, user)
                return HttpResponseRedirect(reverse('blog:index'))
            return render(request, 'blog/login.html', {"msg":"用户名密码错误", "login_form":login_form})

        return render(request, 'blog/login.html', {"login_form":login_form})

class LogoutView(View):
    """
        用户退出
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('blog:index'))
    
class UserProfileView(LoginRequiredMixin,TemplateView):
    """
        用户个人资料
    """
    template_name = 'accounts/profile.html'


class UserUpdateProfileView(LoginRequiredMixin, View):
    """
        修改用户个人资料
    """
    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user)
        return render(request,'accounts/profile_change.html',context={'form':form})

    def post(self, request, *args, **kwargs): 
        update_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            update_form = ProfileForm(instance=request.user)
        return render(request,'accounts/profile_change.html',context={'form':form})

@login_required
def change_profile_view(request):
    if request.method == 'POST':
        # 上传文件需要使用request.FILES
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            # 添加一条信息,表单验证成功就重定向到个人信息页面
            messages.add_message(request,messages.SUCCESS,'个人信息更新成功！')
            return redirect('users:profile')
    else:
        # 不是POST请求就返回空表单
        form = ProfileForm(instance=request.user)
    return render(request,'accounts/profile_change.html',context={'form':form})