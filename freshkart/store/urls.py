from django.urls import path
from . import views

urlpatterns = [
    path('',views.fk_login),
    path('signup',views.signup),
    path('fk_logout',views.fk_logout),
    # ---------------Shop------------------
    path('shop_home',views.shop_home),
]