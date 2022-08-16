from django import forms

from ecommerce.models import Animal, UploadAnimalImages

class UploadAnimalImagesForm(forms.ModelForm):
  class Meta:
    model = UploadAnimalImages
    fields = '__all__'
    
  

class AddNewAnimalForm(forms.ModelForm):
  image_1 = forms.ImageField(label='1st Image',max_length=200, widget=forms.FileInput(attrs={'class': 'form-control'}))
  image_2 = forms.ImageField(label='2nd Image', max_length=200, widget=forms.FileInput(attrs={'class': 'form-control'}))
  image_3 = forms.ImageField(label='3rd Image', max_length=200, widget=forms.FileInput(attrs={'class': 'form-control'}))
  class Meta:
    model = Animal
    exclude = ['quantity']
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
      'category': forms.Select(attrs={'class': 'form-control'}),
      'sex': forms.Select(attrs={'class': 'form-control'}),
      'quantity': forms.TextInput(attrs={'class': 'form-control'}),
      'breed': forms.TextInput(attrs={'class': 'form-control'}),
      'weight': forms.TextInput(attrs={'class': 'form-control'}),
      'price': forms.TextInput(attrs={'class': 'form-control'}),
      'discount': forms.TextInput(attrs={'class': 'form-control'}),
      # 'image_1': forms.FileInput(attrs={'class': 'form-control'}),
    }
    
  def save(self, commit: bool = ...):
    instance = super(AddNewAnimalForm, self).save(commit=False)
    instance.save()
    
      
    upload1 = UploadAnimalImages.objects.create(animal=instance, image=self.cleaned_data.get('image_1'))
    upload1.save()
    upload2 = UploadAnimalImages.objects.create(animal=instance, image=self.cleaned_data.get('image_2'))
    upload2.save()
    upload3 = UploadAnimalImages.objects.create(animal=instance, image=self.cleaned_data.get('image_3'))
    upload3.save()
    
    return instance
      