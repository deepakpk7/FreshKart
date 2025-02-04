from django.urls import path
from . import views

urlpatterns = [
    path('',views.gro_login),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('logout',views.gro_logout),
    # ---------------Shop------------------
    path('register',views.register),
    path('shop_home',views.shop_home),
    path('addproduct',views.add_product),
    path('categoryyy',views.categoryyy),
    path('delete_cat/<id>',views.delete_cat),
    path('view_category/<id>',views.view_category),
    path('details',views.details),
    
    # ---------------User----------
    path('user_home',views.user_home),
    
]