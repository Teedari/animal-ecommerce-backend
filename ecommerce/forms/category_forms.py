from django import forms
from ecommerce.models import Category


class CategoryCreationForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-2'}))
  description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-2', 'col': '2'}))
  class Meta:
    model = Category
    fields = '__all__'