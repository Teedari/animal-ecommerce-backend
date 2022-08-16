from email import message
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
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
  

class ListDeliveryPointsView(generic.ListView):
  model = DeliveryPoint
  template_name = 'dashboard/delivery_point/list_all_delivery_points.html'
  
  
class EditDeliveryPointView(generic.DetailView):
  model = DeliveryPoint
  form_class = DeliveryPointCreationForm
  template_name = 'dashboard/delivery_point/edit_delivery_point.html'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["form"] = self.form_class(initial=kwargs['object'].get_serialized_form_data)
      return context
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(data=request.POST)
    if form.is_valid():
      messages.success(request, 'Updated successfully')
      return UpdateDeliveryPoint.as_view()(request, *args, **kwargs)
    messages.error(request, 'Delivery point update unsuccessful')
    return render(request, self.template_name, {'form': form, 'object': self.get_object()})
      
  
  

class UpdateDeliveryPoint(generic.UpdateView):
  model = DeliveryPoint
  fields =[
    'name',
    'fee',
    'description'
  ]
  
  success_url= '/delivery'
  

