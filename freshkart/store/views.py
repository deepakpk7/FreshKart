from django.shortcuts import render,redirect

# Create your views here.

def index(req):
    return render(req,'index.html')
