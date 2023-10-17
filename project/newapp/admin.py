from django.contrib import admin
from .models import Category,Product,cart,wishlist,order,orderitem
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(order)
admin.site.register(orderitem)

