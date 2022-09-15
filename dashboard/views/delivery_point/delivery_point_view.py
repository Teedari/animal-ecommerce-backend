from email import message
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from ecommerce.models import DeliveryPoint
from ecommerce.forms.delivery_points_form import DeliveryPointCreationForm
from django.contrib import messages

class CreateDeliveryPoints(View):
  template_name='dashboard/delivery_point/create_delivery_point.html'
  form_class = DeliveryPointCreationForm
  
  def get(self, request, **kwargs):
    return render(request, self.template_name, {'form': self.form_class()})
  
  def post(self, request, **kwargs):
    context = {}
    form = self.form_class(data=request.POST)
    if form.is_valid():
      form.save()
      context['form'] = self.form_class()
      messages.success(request, 'Delivery point added successfully')
    else:
      context['form'] = self.form_class(data=request.POST)
      messages.error(request, 'Delivery point added unsuccessful')
    return render(request, self.template_name, context)
  

class ListDeliveryPointsView(UserViewAccessibilityMixin, generic.ListView):
  model = DeliveryPoint
  template_name = 'dashboard/delivery_point/list_all_delivery_points.html'
  is_admin_only = True
  
class EditDeliveryPointView(UserViewAccessibilityMixin, generic.UpdateView):
  model = DeliveryPoint
  form_class = DeliveryPointCreationForm
  template_name = 'dashboard/delivery_point/edit_delivery_point.html'
  success_url = '/delivery'
  is_admin_only = True
  
      
  
  

class UpdateDeliveryPoint(UserViewAccessibilityMixin, generic.UpdateView):
  model = DeliveryPoint
  fields =[
    'name',
    'fee',
    'description'
  ]
  
  success_url= '/delivery'
  
  is_admin_only = True

