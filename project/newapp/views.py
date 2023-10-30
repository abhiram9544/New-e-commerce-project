from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django .http import JsonResponse
from .models import *
from django.contrib import messages
import random

# Create your views here.

def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password')
        password2=request.POST.get('password2')
        if password1 != password2:
            return HttpResponse('your password are not same')
        else:
            my_user=User.objects.create_user(uname,email,password1)
            my_user.save()
            return redirect('loginn') 
    return render (request,'signup.html')


def loginn(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password')
        user=authenticate(request,username=username,password=password1)
        if user is not None:
            login(request,user)
            messages.success(request,'login successfully')
            return redirect('home')
        else:
            return HttpResponse("username or password is incorrect")
    return render (request,'login.html')
 
def home(request):

    trending_product = Product.objects.filter(trending=1)
    context ={'trending_product':trending_product}
    return render (request,'home.html',context)



def logoutpage(request):
    logout(request)
    messages.success(request,'logout successfully')
    return redirect('loginn')

def collections(request):
    category=Category.objects.filter(status=0)
    context={'category':category}
    return render(request,'collections.html',context)


def collectionview(request,slug):

    if(Category.objects.filter(slug=slug,status=0)):
        products=Product.objects.filter(category__slug=slug)
        
        context={'products':products}
    return render(request,'products.html',context)

def productview(request,cate_slug,prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            prod=Product.objects.filter(slug=prod_slug,status=0)
            context={'prod':prod}
    return render (request,'productview.html',context)

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id= int(request.POST.get('product_id'))
            product_check= Product.objects.get(id=prod_id)
            if(product_check):
                if(cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status':"product already in cart"})
                else:
                    prod_qty=int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':'product added cart'})
                    else:
                        return JsonResponse({'status':'only'+str(product_check.quantity) + 'quantity available'})



            else:
                return JsonResponse({'status':'no such product found'})
        else:
            return JsonResponse({'status':'login required'})  
        
    return redirect('/')

def showcart(request):
    Cart=cart.objects.filter(user=request.user)
    context={'Cart':Cart}
    return render(request,'cart.html',context)

def updatecart(request):
    if request.method == 'POST':
        prod_id=int(request.POST.get('product_id'))
        if(cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty=int(request.POST.get('product_qty'))
            Cart=cart.objects.get(product_id=prod_id,user=request.user)
            Cart.product_qty=prod_qty
            Cart.save()
            return JsonResponse({'status':'quantity updated suucessfully'})  
    return redirect('/')



def deletecart(request):

    if request.method == 'POST':
        prod_id=int(request.POST.get('product_id'))
        if(cart.objects.filter(user=request.user,product_id=prod_id)):
            cartitem=cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':'deleted successfully'})  
    return redirect('/')



    

def Wishlist(request):
    wishlistitem=wishlist.objects.filter(user=request.user)
    context={'wishlistitem':wishlistitem}
    return render(request,'wishlist.html',context)
def addtowishlist(request):

    if request.method=='POST':
        if request.user.is_authenticated:
            prod_id=int(request.POST.get('product_id'))
            product_check=Product.objects.get(id=prod_id)
            if(product_check):
                if(wishlist.objects.filter(user=request.user,product_id=prod_id)):
                    return  JsonResponse({'status':'product already in  wishlist '})  
                else:
                    wishlist.objects.create(user=request.user,product_id=prod_id)
                    return  JsonResponse({'status':'product added to  wishlist '}) 
            else:
                return  JsonResponse({'status':'product not found '})
        else:
            return  JsonResponse({'status':'login to continue '})    





    return redirect('/')


def deletewishlist(request):

    if request.method == 'POST':
        prod_id=int(request.POST.get('product_id'))
        if(wishlist.objects.filter(user=request.user,product_id=prod_id)):
            wishlistitem=wishlist.objects.get(product_id=prod_id,user=request.user)
            wishlistitem.delete()
        return JsonResponse({'status':'deleted successfully'})  
    return redirect('/')


def checkout(request):
    cartitems=cart.objects.filter(user=request.user)
    totalprice=0
    for items in cartitems:
        totalprice=totalprice+ items.product.selling_price * items.product_qty
    #auto checkout   
    userprofile=profile.objects.filter(user=request.user).first()
    context={'totalprice':totalprice,'cartitems':cartitems,'userprofile':userprofile}   
    return render (request,'checkout.html',context)


def placeorder(request):
    if request.method=='POST':
        #auto checkout page
        currentuser=User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        
        if not profile.objects.filter(user=request.user):
            userprofile=profile()
            userprofile.user=request.user
            userprofile.phone=request.POST.get('phonenumber')
            userprofile.address=request.POST.get('address')
            userprofile.city=request.POST.get('city')
            userprofile.state=request.POST.get('state')
            userprofile.country=request.POST.get('country')
            userprofile.pincode=request.POST.get('pincode')
            userprofile.save()


        neworder=order()
        neworder.user=request.user
        neworder.fname=request.POST.get('fname')
        neworder.lname=request.POST.get('lname')
        neworder.email=request.POST.get('email')
        neworder.phone=request.POST.get('phonenumber')
        neworder.address=request.POST.get('address')
        neworder.city=request.POST.get('city')
        neworder.state=request.POST.get('state')
        neworder.country=request.POST.get('country')
        neworder.pincode=request.POST.get('pincode')

        neworder.payment_mode=request.POST.get('payment_mode')


        Cart=cart.objects.filter(user=request.user)
        Cart_totalprice=0
        for item in Cart:
            Cart_totalprice=Cart_totalprice+item.product.selling_price*item.product_qty


        neworder.totalprice=Cart_totalprice     
        trackno='abhiram'+str(random.randint(1111111,9999999))
        while order.objects.filter(tracking_no=trackno)is None:
            trackno='abhiram'+str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems=cart.objects.filter(user=request.user)
        for item in neworderitems:
            orderitem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            # to decrese the product quantity from available stock
            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity=orderproduct.quantity-item.product_qty
            orderproduct.save()
        #to clear user cart
        cart.objects.filter(user=request.user).delete()
        messages.success(request,"your order placed")    

    return redirect('home')


def myorders(request):

    orders=order.objects.filter(user=request.user)
    context={'orders': orders}
    return render (request, "orders.html",context)

def orderview(request,t_no):
    Order=order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    Orderitem=orderitem.objects.filter(order=Order)
    context = {'order':Order,'orderitems':Orderitem}

    return render(request, "orderview.html",context)


def productlistajax(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productlist=list(products)
    return JsonResponse (productlist,safe=False)


def searchproducts(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            products=Product.objects.filter(name__contains=searchedterm).first()
            if products:
                return redirect('collections/'+products.category.slug+'/'+products.slug)
            else:
                messages.info(request,"no products found")
                return redirect(request.META.get('HTTP_REFERER'))


    return redirect(request.META.get('HTTP_REFERER'))