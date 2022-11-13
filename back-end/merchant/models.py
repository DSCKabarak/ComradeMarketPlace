from django.db import models
#from django_autoslug.fields import AutoSlugField

class Category(models.Model):

    category_name = models.CharField(max_length=256)
    sub_category = models.CharField(max_length=256)
    #slug = AutoSlugField(unique_by='id', populate_form='category_name')

    def __str__(self):
        category = f'{self.category_name}, {self.sub_category}'
        return category
    
    class Meta:
        db_table = 'categories'


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=("categories"), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'products'
