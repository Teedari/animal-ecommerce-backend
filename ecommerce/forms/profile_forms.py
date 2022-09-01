from unittest import skip
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

attrs = {'class': 'form-control type_2'}

class ProfileUserInfoUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']
    
  def __init__(self, data=None, files=None, *args, **kwargs):
    super().__init__(data, files, *args, **kwargs)
    i = 0
    for _, field in self.fields.items():
      field.widget.attrs = attrs
      
      
      
class ProfileUserPasswordChangeForm(forms.Form):
  current_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs), max_length=200)
  new_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs), max_length=200)

  def clean(self):
    current_password = self.cleaned_data['current_password']
    new_password = self.cleaned_data['new_password']
    if current_password == new_password:
      raise forms.ValidationError('Password change failed, new password must be different from your current password')
    return super().clean()
  
  def change_password(self, user):
    user = User.objects.filter(id = user.id).first()
    try:
      user.set_password(self.cleaned_data['new_password'])
      user.save()
    except Exception as ex:
      raise ex;