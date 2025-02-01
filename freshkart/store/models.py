from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

# Create your models here.


class Category(models.Model):
    category=models.TextField()

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    des=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    img=models.FileField()


class Details(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    weight=models.TextField()
    price=models.IntegerField()
    off_price=models.IntegerField()
    stock=models.IntegerField() 
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def calculate_discounted_price(self):
        """Returns the final price after applying the discount."""
        return self.price - (self.price * (self.discount / 100))

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ForeignKey(Details, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price=models.FloatField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField()
    address=models.TextField()
    street=models.TextField()
    city=models.TextField()
    state=models.TextField()
    pincode=models.IntegerField()
    phone=models.IntegerField()
    message=models.TextField()

class Buy(models.Model):
    details =models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    tot_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(_("Payment Status"), default=PaymentStatus.PENDING,max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_('Signature ID'),max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"