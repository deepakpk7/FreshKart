from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import math,random
import razorpay
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def fk_login(req):
        if 'shop' in req.session:
                return redirect(shop_home)
        if 'user' in req.session:
                return redirect(user_home)
        if req.method=='POST':
                uname=req.POST['uname']
                password=req.POST['password']
                shop=authenticate(username=uname,password=password)
                if shop:
                        login(req,shop)
                        if shop.is_superuser:
                                req.session['shop']=uname   
                                return redirect(shop_home)
                        else:
                                req.session['user']=uname   
                                return redirect(user_home)
                else:
                    messages.warning(req,'Invaild username or password!!!')
                    return redirect(fk_login)
        else:
                return render(req,'login.html')

# ----------------Admin-----------------

def shop_home(req):
    return render(req,'shop/shop.html')







# -------------------User--------------

def user_home(req):
    return render(req,'user/user.html')
