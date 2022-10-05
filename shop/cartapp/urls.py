from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.cartview, name='cartview'),  
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('add_cart_plus/',views.add_cart_plus, name='add_cart_plus'),
    path('delete_carts/<int:product_id>/<int:cart_id>',views.delete_cart_product,name='delete_cart_product'),
    path('delete_cart/<int:product_id>/',views.delete_cart,name='delete_cart'),
    path('add_cartsimple/<int:id>/',views.add_cartsimple, name='add_cartsimple'), 
    path('add_cartplus/<int:product_id>/',views.add_cartplus, name='add_cartplus'),
    path('remove_cartminus/<int:product_id>/',views.remove_cartminus,name ='remove_cartminus' ),
    path('remove_cart/<int:product_id>/',views.remove_cart,name ='remove_cart' ),
    path('apply_coupon',views.apply_coupon,name ='apply_coupon' ),

    
]