from django.shortcuts import render,redirect

# Create your views here.

# admin- freshmart
# pass- fresh
def index(req):
    return render(req,'index.html')
