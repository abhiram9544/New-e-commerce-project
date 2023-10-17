from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('',views.signup,name='signup'),
    path('loginn/',views.loginn,name='loginn'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutpage,name='logout'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:slug>',views.collectionview,name='collectionview'),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productview,name='productview'),
    path('add-to-cart',views.addtocart,name='addtocart'),
    path('cart',views.showcart,name='showcart'),
    path('update-cart',views.updatecart,name='update-cart'),
    path('deletecart',views.deletecart,name='deletecart'),

    path('wishlist',views.Wishlist,name='wishlist'),
    path('add-to-wishlist',views.addtowishlist,name='add-to-wishlist'),
    path('deletewishlist',views.deletewishlist,name='deletewishlist'),

    path('checkout',views.checkout,name='checkout'),
    path('placeorder',views.placeorder,name='placeorder')
   

]