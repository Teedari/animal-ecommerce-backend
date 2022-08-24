from django import forms
from ecommerce.models import Category


class CategoryCreationForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = '__all__'
    widgets ={
      'name': forms.TextInput(attrs={'class': 'form-control mt-2'}),
      'description': forms.Textarea(attrs={'class': 'form-control mt-2', 'col': '2'}),
    }