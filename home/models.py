# models.py
from django.db import models

class YourData(models.Model):
    District = models.CharField(max_length=255)
    Murder =models.IntegerField()
    Hurt  = models.IntegerField()
    AssaultonWomen = models.IntegerField()
    KidnappingandAbduction  = models.IntegerField()
    Rape = models.IntegerField()
    UnlawfulAssembly = models.IntegerField()
    Theft  = models.IntegerField()
    Burglary = models.IntegerField()
    ForgeryCheatingFraud  = models.IntegerField()
    OffencesRelatingtoDocumentsPropertyMarks = models.IntegerField()
    RashDrivingonPublicway  = models.IntegerField()
    CriminalTrespass = models.IntegerField()
    # Add more fields based on your dataset

# class ScamReporting(models.Model):
#     user = models.OneToOneField('accounts.User', on_delete=models.SET_NULL)
#     district = 