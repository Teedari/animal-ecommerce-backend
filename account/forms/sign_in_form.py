from django import forms
from django.contrib.auth import login, authenticate

class SignInForm(forms.Form):
  username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
  
  
  def loginUser(self, request):
    auth = authenticate(request, **self.cleaned_data)
    if not auth:
      raise forms.ValidationError('User does not exist in database')
    login(request, auth)
    