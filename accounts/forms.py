from allauth.account.forms import SignupForm
from django import forms
from .models import *
from django.contrib.auth.models import User

class SimpleSignupForm(SignupForm):
    is_police = models.BooleanField(default=False)
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.is_police = self.cleaned_data['is_police']
        user.save()
        return user
    
USER_TYPE_CHOICES = (
     ('Citizen', 'Citizen'),
    ('Police', 'Police'),
   
)

class CustomSignupForm(SignupForm):
    phone = forms.CharField(
        widget = forms.TextInput)
    district = forms.CharField(
        widget = forms.TextInput)
    class Meta:
        model = User
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone']
        user.district=self.cleaned_data['district']
        user.save()
        return user

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Police



class PoliceSignupForm(forms.ModelForm):
    class Meta:
        model = Police
        fields = ['station_code', 'station_name', 'password','district']


class PoliceLoginForm(forms.ModelForm):
    class Meta:
        model = Police
        fields = ['station_code', 'password']


