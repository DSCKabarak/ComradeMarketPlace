from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from phonenumber_field.phonenumber  import PhoneNumber
from django.conf import settings


class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        ('merchant', 'merchant'),
        ('buyer', 'buyer')
    )
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    bio = models.TextField()
    phone_number = PhoneNumber(blank=False)
    user_type = models.CharField(max_length=90, choices=TYPE_CHOICES)
    avatar = models.FileField(upload_to='user/uploads/avatar/') 
    created_at = models.DateTimeField(auto_now_add=True)
    upadated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.first_name

    def get_avatar_url(self) -> str: #image url
        return self.avatar.url
    
    def get_absolute_url(self):
        return reverse("merchant:user", kwargs={"pk": self.pk})


