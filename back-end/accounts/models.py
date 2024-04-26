from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields["is_superuser"] = False
        extra_fields["is_staff"] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = False

        return self.save_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser should be True")

        extra_fields["is_staff"] = True

        return self.save_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    TYPE_CHOICES = (("", "Select"), ("merchant", "merchant"), ("buyer", "buyer"))
    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    bio = models.TextField()
    is_verified = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, default="07XXXXXXXX")
    user_type = models.CharField(max_length=90, choices=TYPE_CHOICES)
    avatar = models.FileField(upload_to="user/uploads/avatar/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_avatar_url(self) -> str:  # image url
        return self.avatar.url

    class Meta:
        db_table = "users"


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name=("user"),
        on_delete=models.DO_NOTHING
    )
    token = models.CharField(("token"), max_length=25)
    created_at = models.DateTimeField(("created at"), auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        db_table = "email_verification_tokens"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="user", on_delete=models.DO_NOTHING)
    token = models.CharField(("token"), max_length=25)
    created_at = models.DateTimeField("created at", auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        db_table = "password_reset_tokens"
