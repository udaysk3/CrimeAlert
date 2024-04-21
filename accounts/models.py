from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,PermissionsMixin,UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    phone = models.CharField(max_length=254,null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    district = models.CharField(max_length=255)
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    

class Police(AbstractBaseUser):
    station_code = models.CharField(max_length=254)
    station_name = models.CharField(max_length=254)
    district = models.CharField(max_length=255)
    USERNAME_FIELD = 'station_code'
    REQUIRED_FIELDS = ['station_code', 'password']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)