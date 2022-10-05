from distutils.command.upload import upload
from django.db import models
from category .models import Brands, Categoryies
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = AutoSlugField(populate_from=['product_name'] ,unique=True)
    description  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField( validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='photos/products')
    image1 = models.ImageField(upload_to='photos/products')
    image2 = models.ImageField(upload_to='photos/products')
    image3 = models.ImageField(upload_to='photos/products')
    stock        = models.IntegerField(validators=[MinValueValidator(0)])
    Is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Categoryies, on_delete=models.CASCADE)
    brand     = models.ForeignKey(Brands, on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add =True)
    modified_date = models.DateTimeField(auto_now=True)
    discount_price = models.IntegerField(null=True, blank=True ,default= 0)

    
    
    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])
    
    
    # def  __str__(self):
    #     return self.product_name

    def __str__(self):
        return self.product_name
    



class Categoryoffer(models.Model):
    category= models.OneToOneField(Categoryies, related_name='category_offers', on_delete=models.CASCADE)
    discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):   
     return self.category.category_name    


class Productoffer(models.Model):
    product= models.OneToOneField(Product, related_name='product_offers', on_delete=models.CASCADE)
    discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):   
     return self.product.product_name