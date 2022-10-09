from django.urls import reverse
from django.shortcuts import render, redirect
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from account.models import UserProfile
from ecommerce.forms.product_forms import ProductCreationForm, AnimalUpdateForm
from ecommerce.models import Product
from django.views import generic, View
from django.contrib import messages


class AddNewProductView(View):
  template_name = 'dashboard/product/add_product.html'
  form_class = ProductCreationForm
  
  
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {'form': self.form_class()})
  
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(data=request.POST, files=request.FILES, owner=UserProfile.get_user_profile(request.user))
    context = {}
    if form.is_valid():
      instance = form.save()
      # instance.save()
      messages.success(request, 'New Animal Added to stocks')
      context['form'] = self.form_class()
    else:
      context['form'] = form
    
    return render(request, self.template_name, context)
  
  
class ListAllProductView(UserViewAccessibilityMixin, generic.ListView,):
  template_name = 'dashboard/product/list_all_products.html'
  model = Product
  allow_user_profiles = [UserProfile.ADMIN]
  
  
class EditProductView(UserViewAccessibilityMixin, generic.UpdateView):
  template_name = 'dashboard/product/edit_product.html'
  model= Product
  success_url = '/products'
  allow_user_profiles = [UserProfile.ADMIN]
  
  def get_form(self, form_class=None):
    return super().get_form(AnimalUpdateForm)

  

class DeleteProductView(UserViewAccessibilityMixin, generic.DeleteView):
  template_name = 'dashboard/product/list_all_products.html'
  model = Product
  allow_user_profiles = [UserProfile.ADMIN]
  
  def get(self, request, *args, **kwargs):
    obj = self.model.objects.filter(id = kwargs["pk"])
    if obj.exists():
      obj.first().delete()
      messages.success(request, f'Animal Deleted Successful #{kwargs["pk"]}')
    return redirect(reverse('dashboard:animal_list'))
  
