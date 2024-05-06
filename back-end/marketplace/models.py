from django.utils.text import slugify
from django.db import models
from accounts.models import CustomUser
from notifications.notify import send_new_category_notification
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    category = models.CharField(max_length=256)
    sub_category = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        category = f"{self.category}, {self.sub_category}"
        return category
    
    def save(self, *args, **kwargs):
        self.slug  = slugify(f"{self.category}-{self.sub_category}")
        super().save(*args, **kwargs)

    def get_category_name(self):
        return f"{self.category}, {self.sub_category}"

    class Meta:
        db_table = "categories"


@receiver(post_save, sender=Category)
def create_category(sender, instance, created, **kwargs):
    if created:
        send_new_category_notification(instance)


class Product(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.NOTHING)
    category = models.ForeignKey(
        Category, verbose_name=("categories"), on_delete=models.NOTHING
    )
    product_name = models.CharField(max_length=256)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    tag = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, blank=True, null=True)
    brand = models.CharField(max_length=256)
    key_features = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.id}-{self.product_name}")
        super().save(*args, **kwargs)

    

    class Meta:
        db_table = "products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.NOTHING)
    image = models.ImageField(upload_to="uploads/product/images/")
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        return self.image.url

    def __str__(self):
        return self.product.product_name

    class Meta:
        db_table = "images"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "comments"


# class SoldProduct(models.Model):
#     merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='merchant')
#     buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     sold = models.BooleanField(default=False)
#     in_stock = models.BooleanField(default=False)
#     sp_uuid = models.UUIDField(default=uuid.uuid4())
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.sold


#     class Meta:
#         db_table = 'sold_products'


# class ConfirmPurchase(models.Model):
#     merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     purchase_confirmed = models.BooleanField(default=False)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     cp_uuid = models.UUIDField(default=uuid.uuid4())

#     def __str___(self):
#         return self.purchase_confirmed

#     class Meta:
#         db_table = 'confirm_purchases'


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
