from asyncio.windows_events import NULL
from audioop import reverse
import code
from django.db import models

# Create your models here.


class Categoryies(models.Model):
    category_name = models.CharField( max_length=50,null=True)
    description = models.CharField(max_length=200 ,null=True)
    category_image = models.ImageField(upload_to = 'photos/categories',blank=True)
    
    def __str__(self):
        return self.category_name

class Brands(models.Model):
    brandname=models.CharField(max_length=100,unique=True,null=True)

    def __str__(self):
        return self.brandname
    

    # def  get_url(self):
    #     return reverse('product_by_brand',args=self.brandname)

