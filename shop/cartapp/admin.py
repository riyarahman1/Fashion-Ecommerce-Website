from django.contrib import admin
from cartapp.views import Cart,CartItem,couponuseduser,coupon
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(coupon)
admin.site.register(couponuseduser)

