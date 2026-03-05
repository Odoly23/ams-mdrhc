from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout
from users.models import AuditLogin
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.contrib import messages
from urllib.parse import urlparse
from django.urls import resolve
# from ipware import get_client_ip
# from ip2geotools.databases.noncommercial import DbIpCity

# Create your views here.
@login_required
@login_required
def home(request):
    context = {
        "title": "Sistema Manajemento Assets",
        'homeActive':"active",
    }
    return render(request, 'home/indexAdmin.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            AuditLogin.objects.create(user=request.user)
            messages.success(request, f'WELLCOME {user.username}')
            return redirect('home')
        else:
            messages.error(request,'Username ou Password la loos! Favor Prense fali!')
    context = {
        "title":"Pajina Login",
    }
    return render(request,'auth/login.html',context)


@login_required
def logout_view(request):
    logout(request)          
    request.session.flush() 
    return render(request, 'auth/logout.html') 


def error_404(request, exception):
        data = {}
        return render(request,'auth/404.html', data)

def error_500(request):
        data = {}
        return render(request,'auth/500.html', data)