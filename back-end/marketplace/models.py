import json
import uuid

from autoslug import AutoSlugField
from django.db import models

from accounts.models import CustomUser


class Category(models.Model):
    category_name = models.CharField(max_length=256)
    sub_category = models.CharField(max_length=256)
    slug = AutoSlugField(unique_with="id", populate_from="category_name")

    def __str__(self):
        category = f"{self.category_name}, {self.sub_category}"
        return category

    class Meta:
        db_table = "categories"

    def get_absolute_url(self):
        return self.name


class Product(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name=("categories"), on_delete=models.CASCADE
    )
    product_name = models.CharField(max_length=256)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    tag = models.CharField(max_length=256)
    slug = AutoSlugField(unique_with="id", populate_from="product_name")
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
        db_table = "products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/product/images/")
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        return self.image.url

    def __str__(self):
        return self.name

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


class Notification(models.Model):
    """
    Notification model to store notifications for users. Has fields for type, recipients, content, sent_at, and read.
    """

    class SentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_sent=True)

    class NotSentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_sent=False)

    TYPE_CHOICES = [
        ("product_added", "Product Added"),
        ("product_sold_out", "Product Sold Out"),
        ("product_back_in_stock", "Product Back in Stock"),
        ("purchase_initiated", "Purchase Initiated"),
        ("purchase_confirmed", "Purchase Confirmed"),
        ("purchase_pending", "Purchase Pending"),
        ("purchase_completed", "Purchase Completed"),
        ("purchase_cancelled", "Purchase Cancelled"),
    ]

    notification_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="product_added"
    )
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.TextField()
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    emailed = SentManager()  #  custom manager for sent notifications.
    not_emailed = NotSentManager()  # custom manager for not sent notifications.

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.email}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        default_manager_name = "objects"
