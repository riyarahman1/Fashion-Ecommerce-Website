
from django.db import models
from accounts.models import Account
from product.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE)
    cart        =   models.ForeignKey(Cart,on_delete=models.CASCADE ,null=True)
    quantity    =   models.IntegerField(null=True)
    cartprice = models.FloatField(null = True)
    is_active   =   models.BooleanField(default=True)

    def sub_total(self):
        if self.product.discount_price:
           return self.product.discount_price * self.quantity
        else:   
           return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name


class coupon(models.Model):
    coupon_code = models.CharField(max_length=50,unique=True)
    discount_percentage = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_code



class couponuseduser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)

    coupon = models.ForeignKey(coupon, on_delete=models.CASCADE,null=True)
   
   
   
    def __str__(self):
        return self.user.username