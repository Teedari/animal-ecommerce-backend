from django.urls import reverse
from django.shortcuts import render, redirect
from ecommerce.forms.animal_forms import AddNewAnimalForm
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
      # instance.image_slug_1 = request.POST.get('upload_image_1', "")
      # instance.image_slug_2 = request.POST.get('upload_image_2', "")
      instance.save()
      messages.success(request, 'New Animal Added to stocks')
      context['form'] = self.form_class()
    else:
      context['form'] = form
    
    return render(request, self.template_name, context)
  
  
class ListAnimalsView(generic.ListView,):
  template_name = 'dashboard/animal/list_all_animals.html'
  model = Animal
  
  
class AnimalEditView(generic.UpdateView):
  pass

class AnimalDeleteView(generic.DeleteView):
  template_name = 'dashboard/animal/list_all_animals.html'
  model = Animal
  
  def get(self, request, *args, **kwargs):
    # breakpoint()
    obj = self.model.objects.filter(id = kwargs["pk"])
    if obj.exists():
      obj.first().delete()
      messages.success(request, f'Animal Deleted Successful #{kwargs["pk"]}')
    return redirect(reverse('dashboard:animal_list'))
  
