from django.db import models
from autoslug import AutoSlugField
import uuid
from accounts.models import CustomUser
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=256)
    sub_category = models.CharField(max_length=256)
    slug = AutoSlugField(unique_with='id', populate_from='category_name')

    def __str__(self):
        category = f'{self.category_name}, {self.sub_category}'
        return category
    
    class Meta:
        db_table = 'categories'

    def get_absolute_url(self):
        return self.name


class Product(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=("categories"), on_delete=models.CASCADE)
    product_name = models.CharField(max_length=256)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    tag = models.CharField(max_length=256)
    slug = AutoSlugField(unique_with='id', populate_from='product_name')
    brand = models.CharField(max_length=256)
    key_features = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.name

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'products'



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/images/')
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_image_url(self):
        return self.image.url

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'images'


class SoldProduct(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='merchant')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=False)
    sp_uuid = models.UUIDField(default=uuid.uuid4())
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.sold

    
    class Meta:
        db_table = 'sold_products'
    

class ConfirmPurchase(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purchase_confirmed = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cp_uuid = models.UUIDField(default=uuid.uuid4())

    def __str___(self):
        return self.purchase_confirmed
    
    class Meta:
        db_table = 'confirm_purchases'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_uuid = models.UUIDField(default=uuid.uuid4())

    def __str__(self):
        return self.comment
    
    class Meta:
        db_table = 'comments'