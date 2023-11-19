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
    
    USER_TYPE_CHOICES = (
     ('Citizen', 'Citizen'),
    ('Police', 'Police'),
   
        )
    user_type = models.CharField(max_length=10,
                                      choices=USER_TYPE_CHOICES,
                                      default='Citizen')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)