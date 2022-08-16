from random import choices
from django import forms
from django.contrib.auth.models import User
from secrets import token_urlsafe

from account.models import UserProfile

class CustomUserCreationForm(forms.ModelForm):
  user_role = forms.ChoiceField(choices=UserProfile.USER_ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

  
  class Meta:
    model = User
    fields = ('username', 'email')
    
    widgets ={
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }
    
    
  
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
      UserProfile.create_user(user, self.cleaned_data['user_role'])
    except Exception as err:
      print(err)
  
    return {
      'user': user,
      'user_role': self.cleaned_data['user_role'],
      'generated_password': password
    }
    