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
    user_type = forms.CharField( 
        widget=forms.Select(choices=USER_TYPE_CHOICES))
    phone = forms.CharField(
        widget = forms.TextInput)
    class Meta:
        model = User
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.user_type = self.cleaned_data['user_type']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user
