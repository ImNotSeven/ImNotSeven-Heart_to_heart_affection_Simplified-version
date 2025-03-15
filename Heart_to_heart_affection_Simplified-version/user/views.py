from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from .forms import registry,edit
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .models import user_extend
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method =='POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',{'错误':'用户名或密码错误'})
        else:
            login(request,user)
            return redirect("/home/")
    else:
        return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("/home/")

def register(request):
    if request.method =='POST':
        createform=registry(request.POST)
        if createform.is_valid():
            createform.save()
            user=authenticate(username=createform.cleaned_data['username'],password=createform.cleaned_data['password1'])
            user_extend(user=user,name=createform.cleaned_data['name'],nickname=createform.cleaned_data['nickname'],phone=createform.cleaned_data['phone']).save()
            return redirect("/user/login")
    else:
        createform=registry()
    value={'createform':createform}
    return render(request, "register.html",value)

@login_required(login_url='/user/login')
def user_center(request):
    value={'user':request.user}
    return render(request,'user_center.html',value)

@login_required(login_url='/user/login')
def edit_profile(request):
    if request.method == 'POST':
        edit_form = edit(request.POST,instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            request.user.user_extend.name=edit_form.cleaned_data['name']
            request.user.user_extend.nickname=edit_form.cleaned_data['nickname']
            request.user.user_extend.phone=edit_form.cleaned_data['phone']
            request.user.user_extend.save()
            # user = authenticate(username=edit_form.cleaned_data['username'],
            #                     password=edit_form.cleaned_data['password1'])
            # user_extend(user=user, 姓名=edit_form.cleaned_data['姓名'], 昵称=edit_form.cleaned_data['昵称'],
            #             手机号=edit_form.cleaned_data['手机号']).save()
            return redirect("/user/user_center")
    else:
        edit_form = edit(instance=request.user)
    value = {'edit_form': edit_form,'user':request.user}
    return render(request, "edit_profile.html", value)

@login_required(login_url='/user/login')
def change_password(request):
    if request.method == 'POST':
        change_form = PasswordChangeForm(data=request.POST, user=request.user)
        if change_form.is_valid():
            change_form.save()

            return redirect("/user/login")
    else:
        change_form = PasswordChangeForm(user=request.user)
    value = {'change_form': change_form, 'user': request.user}
    return render(request, "change_password.html", value)

