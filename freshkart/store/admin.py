from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Details)
admin.site.register(Address)
admin.site.register(Order)