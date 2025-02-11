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

def gro_login(req):
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
                    return redirect(gro_login)
        else:
                return render(req,'login.html')

def OTP(req):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def register(req):
    if req.method=='POST':
        email=req.POST['email']
        name=req.POST['uname']
        password=req.POST['password']
        otp=OTP(req)
        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect(register)
        else:
            send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
        # try:
        #     data=User.objects.create_user(first_name=uname,email=email,username=email,password=password)
        #     data.save()
        #     return redirect(gro_login)
        # except:
        #     messages.warning(req,'Email Already Exists!!')
        #     return redirect(register)
    else:
        return render(req,'register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        uotp=req.POST['uotp']
        if uotp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req, "OTP verified successfully. You can now log in.")
            return redirect(gro_login)
        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,'pass':password,'email':email,'otp':otp})

def gro_logout(req):
    logout(req)
    req.session.flush()
    return redirect(gro_login)

# ----------------Admin-----------------

def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()  
        data1=Details.objects.all()
        return render(req,'shop/shop.html',{'data':data,'data1':data1})
    else:
        return redirect(gro_login)

def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['p_id']
            name=req.POST['name']
            descri=req.POST['description']
            categories=req.POST['p_categories']
            img=req.FILES['p_img']
            data=Product.objects.create(pid=pid,name=name,img=img,des=descri,category=Category.objects.get(category=categories))
            data.save()
            return redirect(details)
        else:
            data=Category.objects.all()        
            return render(req,'shop/addproduct.html',{'data':data})
    else:
        return redirect(gro_login)
def categoryyy(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            category=req.POST['p_categories']
            data=Category.objects.create(category=category)
            data.save()
            return redirect(categoryyy)
        else:
            data=Category.objects.all()
            return render(req,'shop/category.html',{'data':data})
    else:
         return redirect(gro_login)
    
def delete_cat(req,id):
     data=Category.objects.get(pk=id)
     data.delete()
     return redirect(categoryyy)

def view_category(req,id):
    category = Category.objects.get(pk=id)
    details = Details.objects.filter(product__category=category)
    return render(req, 'user/view_cat.html', {'category': category,'details': details})

def details(req):
    if req.method == 'POST':
            products=req.POST['p_id']
            weight=req.POST['p_weight']
            price=req.POST['p_price']
            offprice=req.POST['of_price']
            stock=req.POST['p_stock']
            data=Details.objects.create(weight=weight,price=price,off_price=offprice,stock=stock,product=Product.objects.get(pid=products))
            data.save()
            return redirect(shop_home)
    else:
            data=Product.objects.all()
            return render(req,'shop/details.html',{'data':data})

def edit_product(req,id):
    if req.method=='POST':
        pid=req.POST['p_id']
        name=req.POST['name']
        descri=req.POST['description']
        img=req.FILES.get('p_img')
        if img:
            Product.objects.filter(pk=id).update(pid=pid,name=name,descri=descri)
            data=Product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=id).update(pid=pid,name=name,des=descri)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=id)      
        return render(req,'shop/edit.html',{'data':data})
    
def editdetails(req,pid):
    if req.method == 'POST':
        details=req.POST['d_id']
        product=req.POST['p_id']
        weight=req.POST['p_weight']
        price=req.POST['p_price']
        offprice=req.POST['of_price']
        stock=req.POST['p_stock']
        Details.objects.filter(pk=details).update(product=Product.objects.get(pk=product),weight=weight,price=price,off_price=offprice,stock=stock)
        return redirect(shop_home)
    else:      
        data=Details.objects.filter(product=pid)
        data1=Product.objects.get(pk=pid)
        return render(req,'shop/editdetails.html',{'data':data,'data1':data1}) 
    
def deletedetails(req,pid):
     data=Details.objects.get(pk=pid)
     data.delete()
     return redirect(shop_home)

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def bookings(req):
    bookings=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'bookings':bookings})





# -------------------User--------------

def user_home(req):
    if 'user' in req.session:
        product=Product.objects.all()
        data=Details.objects.all()
        data1=Category.objects.all()
        return render(req,'user/user.html',{'products':product,'data':data,'data1':data1})
    else:
         return redirect(gro_login)
     
def view_pro(req,pid):
    if 'user' in req.session:
        data=Product.objects.get(pk=pid)
        data1=Details.objects.filter(product=pid)
        data2=Details.objects.get(product=pid,pk=data1[0].pk)
        cat=Category.objects.all()
        if req.GET.get('dis'):
                dis=req.GET.get('dis')
                data2=Details.objects.get(product=pid,pk=dis)
        return render(req,'user/view_product.html',{'data':data,'data1':data1,'data2':data2,'cat':cat})
    else:
         return redirect(gro_login)
     
     
def add_to_cart(req,id):
    details = Details.objects.get(pk=id)
    user = User.objects.get(username=req.session['user'])
    try:
        cart = Cart.objects.get(details=details, user=user)
        cart.quantity += 1
        cart.price=cart.details.off_price*cart.quantity
        cart.save()
    except:
        price=details.off_price
        data = Cart.objects.create(details=details,user=user,quantity=1,price=price)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        data = Cart.objects.filter(user=user)
        total=0
        for i in data:
            total+=i.price*i.quantity
        cat=Category.objects.all()
        return render(req, 'user/cart.html', {'cart': data,'cat':cat,'total':total})
    else:
         return redirect(gro_login)

def remove_item(req,id):
    data=Cart.objects.get(pk=id)
    data.delete()
    return redirect(view_cart)

def qty_add(req,cid):
    try:
        data=Cart.objects.get(pk=cid)
        if data.details.stock > data.quantity:
            data.quantity+=1
            data.save()
        else:
            messages.warning(req, "Cannot increase quantity. Stock unavailable.")
    except Cart.DoesNotExist:
        messages.error(req, "Cart item not found.")
    return redirect(view_cart)

def qty_sub(req,cid):
    data=Cart.objects.get(pk=cid)
    data.quantity-=1
    data.save()
    if data.quantity==0:
        data.delete()
    return redirect(view_cart)

def buyNow(req,pid):
    if 'user' in req.session:
        prod=Details.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary",prod=prod.pk,data=data)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                address=req.POST['address']
                street=req.POST['street']
                city=req.POST['city']
                state=req.POST['state']
                pin=req.POST['pin']
                phone=req.POST['phone']
                data=Address.objects.create(user=user,name=name,address=address,street=street,city=city,state=state,pincode=pin,phone=phone)
                data.save()
                return redirect("orderSummary",prod=prod.pk,data=data)
            else:
                return render(req,"user/address.html")
    else:
        return redirect(gro_login) 
    
def orderSummary(req,prod,data):
    if 'user' in req.session:
        prod=Details.objects.get(pk=prod)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method == 'POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
            print(pay)
        else:
            cat=Category.objects.all()
            return render(req,'user/order.html',{'prod':prod,'data':data,'cat':cat})
        print(prod.pk)
        req.session['address']=addr.pk
        req.session['detail']=prod.pk
        if pay == 'paynow':
            return redirect("payment")    
        else:
            return redirect("buy_pro")  
    else:
        return redirect(gro_login)


def address(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phone']
            house=req.POST['address']
            street=req.POST['street']
            city=req.POST['city']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phone=phn,address=house,city=city,street=street,pincode=pin,state=state)
            data.save()
            return redirect(address)
        else:
            return render(req,"user/address.html",{'data':data})
    else:
        return redirect(gro_login) 
    
def delete_address(req,pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(address)
    else:
        return redirect(gro_login)
    

def carbuy(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        price=0
        total=0
        for i in cart:
            price+=(i.details.price)*i.quantity
            price=price
            total+=(i.details.off_price)*i.quantity
            total=total
        data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary2",price=price,total=total)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phone']
                house=req.POST['address']
                street=req.POST['street']
                city=req.POST['city']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phone=phn,address=house,city=city,street=street,pincode=pin,state=state)
                data.save()
                return redirect("orderSummary2",price=price,total=total)
            else:
                return render(req,"user/address.html")
    else:
        return redirect(gro_login) 
    
def orderSummary2(req,price,total):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        carts=Cart.objects.filter(user=user)# return render(req,'user/orderSummary2.html',{'cart':cart,'data':data,'discount':discount,'price':price,'total':total})
        if req.method == 'POST':
            address=req.POST['address']
            pay1=req.POST['payable']
            addr=Address.objects.get(user=user,pk=address)
        else:
            cat=Category.objects.all()
            return render(req,'user/cartorder.html',{'data2':carts,'data':data,'price':price,'total':total,'cat':cat})
        req.session['address']=addr.pk
        # req.session['detail']=carts.pk
        if pay1 == 'paynow':
            return redirect("payment2")    
        else:
            return redirect(book2)    
    else:
        return redirect(gro_login)

def payment2(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        cat=Category.objects.all()
        price=0
        for i in cart:
            price+=(i.details.off_price)*i.quantity
        total=price
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        amount = total
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment2.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback2",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return redirect(gro_login) 
def book2(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        price=0
        for i in cart:
            price=i.price*i.quantity
            data=Buy.objects.create(user=i.user,details=i.details,quantity=i.quantity,tot_price=price,address=Address.objects.get(pk=req.session['address']))
            data.save()
        cart.delete()
        return redirect(user_bookings)
    else:
        return redirect(gro_login)
    
def user_bookings(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        bookings=Buy.objects.filter(user=user)[::-1]
        cat=Category.objects.all()
        return render(req,'user/user_bookings.html',{'bookings':bookings,'cat':cat})
    else:
         return redirect(gro_login)
     
def deleteBookings(req,pid):
    if 'user' in req.session:
        data=Buy.objects.get(pk=pid)
        data.delete()
        return redirect(user_bookings)
    else:
        return redirect(gro_login)
