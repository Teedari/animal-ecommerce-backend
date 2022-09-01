from django.urls import reverse
from django.shortcuts import render, redirect
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from account.models import UserProfile
from ecommerce.forms.animal_forms import AddNewAnimalForm, AnimalUpdateForm
from ecommerce.models import Animal
from django.views import generic, View
from django.contrib import messages


class AddNewAnimalView(View):
  template_name = 'dashboard/animal/add_animal.html'
  form_class = AddNewAnimalForm
  
  
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {'form': self.form_class()})
  
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST, request.FILES)
    context = {}
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      messages.success(request, 'New Animal Added to stocks')
      context['form'] = self.form_class()
    else:
      context['form'] = form
    
    return render(request, self.template_name, context)
  
  
class ListAnimalsView(UserViewAccessibilityMixin, generic.ListView,):
  template_name = 'dashboard/animal/list_all_animals.html'
  model = Animal
  allow_user_profiles = [UserProfile.ADMIN]
  
  
class AnimalEditView(UserViewAccessibilityMixin, generic.UpdateView):
  template_name = 'dashboard/animal/edit_animal.html'
  model= Animal
  success_url = '/animals'
  allow_user_profiles = [UserProfile.ADMIN]
  
  def get_form(self, form_class=None):
    return super().get_form(AnimalUpdateForm)

  

class AnimalDeleteView(UserViewAccessibilityMixin, generic.DeleteView):
  template_name = 'dashboard/animal/list_all_animals.html'
  model = Animal
  allow_user_profiles = [UserProfile.ADMIN]
  
  def get(self, request, *args, **kwargs):
    obj = self.model.objects.filter(id = kwargs["pk"])
    if obj.exists():
      obj.first().delete()
      messages.success(request, f'Animal Deleted Successful #{kwargs["pk"]}')
    return redirect(reverse('dashboard:animal_list'))
  
