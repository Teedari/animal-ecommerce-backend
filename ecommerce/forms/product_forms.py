from dataclasses import field
from django import forms

from ecommerce.models import Product, ProductImage

# class UploadAnimalImagesForm(forms.ModelForm):
#   class Meta:
#     model = UploadAnimalImages
#     fields = '__all__'
    
attrs = {'class': 'form-control'}

class ProductCreationForm(forms.ModelForm):
  image_1 = forms.ImageField(label='1st Image')
  image_2 = forms.ImageField(label='2nd Image')
  class Meta:
    model = Product
    exclude = ['quantity', 'owner']
    
    
  def __init__(self, data=None, files=None, owner=None, *args, **kwargs) -> None:
    super().__init__(data, files, *args, **kwargs)
    self.owner = owner
    for _, field in self.fields.items():
      field.widget.attrs = attrs
  
    
  def save(self, commit: bool = ...):
    instance = super(ProductCreationForm, self).save(commit=False)
    instance.owner = self.owner
    instance.save()

    ProductImage.create_product_image(product=instance, image=self.cleaned_data.get('image_1'))
    ProductImage.create_product_image(product=instance, image=self.cleaned_data.get('image_2'))
    return instance
      

class AnimalUpdateForm(forms.ModelForm):
  
  class Meta:
    model = Product
    exclude = ['image_slug_1', 'image_slug_2', 'quantity', 'owner']
    
  def __init__(self, data=None, files=None, *args, **kwargs):
    super().__init__(data=data, files=files, *args, **kwargs)
    for _, fields in self.fields.items():
      if _ == 'description':
        fields.widget = forms.Textarea()
      fields.widget.attrs = {'class': 'form-control'}
    