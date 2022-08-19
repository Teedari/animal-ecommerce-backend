from random import choices
from django import forms
from django.contrib.auth.models import User, Group
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
    
    data = self.cleaned_data
    password = token_urlsafe()
    user = super().save(commit=False)
    user.is_active = True
    user.set_password(password)
    
    if self.cleaned_data['user_role'] == UserProfile.ADMIN:
      user.is_superuser = True
      user.is_staff = True
      data['user_role'] = UserProfile.ADMIN
      
    elif data['user_role'] == UserProfile.AGENT:
      data['user_role'] = UserProfile.AGENT
      
    elif data['user_role'] == UserProfile.CUSTOMER:
      data['user_role'] = UserProfile.CUSTOMER
    else:
      data['user_role'] = UserProfile.UNKNOWN
      
    group, exists = Group.objects.get_or_create(name=data['user_role']) 
    if group:
      user.groups.add(group)
    user.save()
    
    try:
      UserProfile.create_user(user, data['user_role'])
    except Exception as err:
      print(err)
  
    return {
      'user': user,
      'user_role': data['user_role'],
      'generated_password': password
    }
    