from django import forms
from ecommerce.models import DeliveryPoint


class DeliveryPointCreationForm(forms.ModelForm):
  class Meta:
    model = DeliveryPoint
    exclude = ['userprofile',]
    
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'fee': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
    }