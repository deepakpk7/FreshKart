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
        
def OTP(req):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def signup(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        # send_mail('Welcome to ElectronicEra!',
        #           """
        #           Dear user,

        #             Thank you for registering with ElectronicEra! We are excited to have you on board.

        #             Your account has been successfully created, and you can start shopping for the best electronics in the market!

        #             Quote of the day: "The best way to predict the future is to invent it." – Alan Kay

        #             Feel free to contact us if you have any questions.

        #             Best regards,
        #             ElectronicEra Team
        #           """, settings.EMAIL_HOST_USER, [email])
        try:
            data=User.objects.create_user(first_name=uname,email=email,
                                        username=email,password=pswd)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(signup)
        return redirect(fk_login)
    else:
        return render(req,'signup.html')

# def signup(req):
#     if req.method=='POST':
#         name=req.POST['uname']
#         email=req.POST['email']
#         password=req.POST['password']
#         # otp=OTP(req)
#         # if User.objects.filter(email=email).exists():
#         #     messages.error(req, "Email is already in use.")
#         #     return redirect(register)
#         # else:
#         #     send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
#         #     messages.success(req, "Registration successful. Please check your email for OTP.")
#         #     return redirect("validate",name=name,password=password,email=email,otp=otp)
#         try:
#             data=User.objects.create_user(first_name=name,email=email,username=email,password=password)
#             data.save()
#             return redirect(fk_login)
#         except:
#             messages.warning(req,'Email Already Exists!!')
#             return redirect(signup)
#     else:
#         return render(req,'signup.html')
        
def signup(req):
        return render(req,'signup.html')

def fk_logout(req):
    logout(req)
    req.session.flush()
    return redirect(fk_login)
# ----------------Admin-----------------

def shop_home(req):
    return render(req,'shop/shop.html')








# -------------------User--------------

def user_home(req):
    return render(req,'user/user.html')
