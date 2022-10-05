from django.contrib import admin
from order.models import Payment,Order,OrderProduct
# Register your models here.


admin.site.register(Payment) 
admin.site.register(OrderProduct) 
admin.site.register(Order) 
