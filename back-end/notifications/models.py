from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Notification(models.Model):
    """
    The Notification model represents a notification that can be sent to a user.

    Attributes:
        notification_type (str): The type of the notification. Choices are defined in TYPE_CHOICES.
        recipient (CustomUser): The user who will receive the notification.
        subject (str): The subject of the notification.
        content (str): The email content of the notification.
        description: The description of the notification that will be displayed to the user.
        is_read (bool): A flag indicating whether the notification has been read by the recipient.
        is_sent (bool): A flag indicating whether the notification has been sent to the recipient.
        sent_at (datetime): The time when the notification was sent.

    Managers:
        objects (Manager): The default manager that includes all notifications.
        emailed (SentManager): A custom manager that includes only the notifications that have been sent.
        not_emailed (NotSentManager): A custom manager that includes only the notifications that have not been sent.
    """

    class SentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_sent=True)

    class NotSentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_sent=False)

    TYPE_CHOICES = [
        ("category_added", "Category Added"),
        ("category_updated", "Category Updated"),
        ("product_added", "Product Added"),
        ("product_sold_out", "Product Sold Out"),
        ("product_back_in_stock", "Product Back in Stock"),
        ("purchase_initiated", "Purchase Initiated"),
        ("purchase_confirmed", "Purchase Confirmed"),
        ("purchase_pending", "Purchase Pending"),
        ("purchase_completed", "Purchase Completed"),
        ("purchase_cancelled", "Purchase Cancelled"),
        ("purchase_refunded", "Purchase Refunded"),
    ]

    notification_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="product_added"
    )
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.TextField()
    content = models.TextField()
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    emailed = SentManager()  #  custom manager for sent notifications.
    not_emailed = NotSentManager()  # custom manager for not sent notifications.

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.email}"

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        default_manager_name = "objects"
