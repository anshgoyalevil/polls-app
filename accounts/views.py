from email import message
from django.shortcuts import render
from accounts.forms import Signupform
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login

def register(request):
    if request.method == 'POST':
      fm=Signupform(request.POST)
      if fm.is_valid():
        user_email=fm.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            message.error(request,"Email already exist")
            return render(request,'accounts/register.html',{'form':fm})
        fm.save()
        return HttpResponseRedirect(reverse("login"))
    else:
      fm=Signupform()
    return render(request,'accounts/register.html',{'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                user_name=fm.cleaned_data['username']
                user_password=fm.cleaned_data['password']
                user=authenticate(username=user_name,password=user_password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect(reverse("index"))
        else:
            fm=AuthenticationForm()
        return render(request,'accounts/login.html',{'form':fm})
    else:
        return HttpResponseRedirect(reverse("index"))


        