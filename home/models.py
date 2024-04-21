# models.py
from django.db import models

from accounts.models import User
from django.conf import settings
class ScamReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    scam_description = models.TextField()
    image = models.ImageField(upload_to='report/')

    




class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

