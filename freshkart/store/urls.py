from django.urls import path
from . import views

urlpatterns = [
    path('',views.gro_login),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('logout',views.gro_logout),
    # ---------------Shop------------------
    path('shop_home',views.shop_home),
    path('addproduct',views.add_product),
    path('categoryyy',views.categoryyy),
    path('delete_cat/<id>',views.delete_cat),
    path('view_category/<id>',views.view_category),
    path('details',views.details),
    path('edit/<id>',views.edit_product),
    path('delete/<pid>',views.delete_product),
    path('editdetails/<pid>',views.editdetails),
    path('delete_details/<pid>',views.deletedetails),
    path('viewpro/<pid>',views.view_pro),
    path('bookings',views.bookings),
    
    # ---------------User----------
    path('user_home',views.user_home),
    
]