from django.db import models
from autoslug import AutoSlugField

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
    category = models.ForeignKey(Category, verbose_name=("categories"), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    tag = models.CharField(max_length=256)
    slug = AutoSlugField(unique_with='id', populate_from='name')
    brand = models.CharField(max_length=256)
    key_features = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.name


    def __str__(self):
        return self.name