from django import forms
from .models import ScamReport

class ScamReportForm(forms.ModelForm):
    class Meta:
        model = ScamReport
        fields = ['district', 'scam_description', 'image']
