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
    path('add_to_cart/<id>',views.add_to_cart),
    path('cart',views.view_cart),
    path('remove_item/<id>',views.remove_item),
    path('qty_add/<cid>',views.qty_add),
    path('qty_sub/<cid>',views.qty_sub),
    path('buynow/<pid>',views.buyNow),
    path('address',views.address),
    path('buycart',views.carbuy),
    
    
]