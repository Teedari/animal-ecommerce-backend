from django.views import View, generic
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from ecommerce.forms.admin_user_creation_from import CustomUserCreationForm




class CreateNewUserAdminView(View):
  template_name = 'dashboard/user/create_admin_user.html'
  form_class = CustomUserCreationForm
  
  def get(self, request, *args, **kwargs):
    
    return render(request, self.template_name, {'form': self.form_class()})
  
  
  def post(self, request, *args, **kwargs):
    context = {}
    form = self.form_class(data=request.POST)
    if form.is_valid():
      instance = form.save()
      context['data'] = instance
      context['form'] = self.form_class()
    else: 
      context['form'] = form
      messages.error(request, 'User Admin Creation Failed')
    return render(request, self.template_name, context)