from django.urls import path
from . import views

urlpatterns = [
    path('',views.gro_login),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('logout',views.gro_logout),
    # ---------------Shop------------------
    path('register',views.register),
    path('shop_home',views.shop_home),
    
    # ---------------User----------
    path('user_home',views.user_home),
    
]