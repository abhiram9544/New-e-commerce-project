from django.db import models
from django.contrib.auth.models import User
import datetime
import os
# Create your models here.

def get_file_path(request,filename):
    original_filename=filename
    nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0=default,1=hidden')
    trending=models.BooleanField(default=False,help_text='0=default,1=Trending')
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.TextField(max_length=500,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self) :
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    product_image1=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    product_image2=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    product_image3=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    small_description=models.CharField(max_length=150,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    product_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0=default,1=hidden')
    trending=models.BooleanField(default=False,help_text='0=default,1=Trending')
    tag=models.CharField(max_length=150,null=False,blank=False)
   
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self) :
        return self.name
    

class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)



class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=150,null=False)
    lname=models.CharField(max_length=150,null=False)
    email=models.EmailField(max_length=150,null=False)
    phone=models.CharField(max_length=150,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    totalprice=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250, null=True)
    orderstatuses=(
        ('pending','pendibg'),
        ('out for shipping','out for shipping'),
        ('completed','completed')
    )
    status=models.CharField(max_length=150,choices=orderstatuses,default='pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id,self.tracking_no)
    

class orderitem(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    def __str__(self):
        return '{}-{}'.format(self.order.id,self.order.tracking_no)
    
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username