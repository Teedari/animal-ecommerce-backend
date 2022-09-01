from random import choices
from unittest import skip
from django import forms
from django.contrib.auth.models import User
from secrets import token_urlsafe

from account.models import UserProfile
from ecommerce.models import DeliveryPoint

class CustomUserCreationForm(forms.ModelForm):
  user_role = forms.ChoiceField(choices=UserProfile.USER_ROLES, widget=forms.Select(attrs={'class': 'form-control'}))
  delivery_location = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=False)
  
  class Meta:
    model = User
    fields = ('username', 'email')
    
    widgets ={
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }
    
  def __init__(self, data=None, files=None, *args, **kwargs) -> None:
    super().__init__(data, files, *args, **kwargs)
    locations = DeliveryPoint.objects.all()
    # breakpoint()
    # self.fields['delivery_location'].={'class': 'form-control'}
    self.fields['delivery_location'].choices = [(location.id,location.name) for location in locations ]
  
  def save(self, commit=False):
    password = token_urlsafe()
    user = super().save(commit=False)
    user.is_staff = True
    user.is_active = True
    user.set_password(password)
    
    if self.cleaned_data['user_role'] == UserProfile.ADMIN:
      user.is_superuser = True
    user.save()
    
    try:
      profile = UserProfile.create_user(user, self.cleaned_data['user_role'])
      # breakpoint()
      if self.cleaned_data['user_role'] == UserProfile.AGENT:
        for location in self.cleaned_data.get('delivery_location'):
          point = DeliveryPoint.objects.filter(id = location)
          if not point:
            skip
          point = point.first()
          point.userprofile.add(profile)
          point.save()
    except Exception as err:
      print(err)
  
    return {
      'user': user,
      'user_role': self.cleaned_data['user_role'],
      'generated_password': password
    }
    