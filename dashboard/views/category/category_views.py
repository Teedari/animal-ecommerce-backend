from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DeleteView
from django.views import View
from ecommerce.forms.category_forms import CategoryCreationForm
from django.contrib import messages
from ecommerce.models import Category
# Create your views here.

class CreateCategory(View):
  model = Category
  template_name = 'dashboard/category/create_category.html'
  form_class = CategoryCreationForm
  
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {'form': self.form_class()})
  
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(data=request.POST)
    context = {}
    if not form.is_valid():
      messages.error(request, 'Category create unsuccessful, try again')
      context['form'] = form
    else:
      form.save()
      messages.success(request, 'Category created successfully!!')
      context['form'] = self.form_class()

    return render(request, self.template_name, context)
  
  
class ListCategories(ListView):
  model = Category
  template_name = 'dashboard/category/list_all_category.html'
  
  
class DeleteCategory(View):
  model = Category
  template_name = 'dashboard/category/list_all_category.html'
   
  def get(self, request, *args, **kwargs):
    if self.model.remove(int(kwargs['pk'])):
      messages.success(request, f'Category #{kwargs["pk"]} is deleted')
    else:
      messages.error(request, f'Category #{kwargs["pk"]} delete unsuccessful')
    return redirect(reverse('dashboard:category_list'))
  