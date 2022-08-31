from django.views import View, generic
from ecommerce.forms.order_forms import StatusUpdateForm
import ecommerce.models as md
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

class ListOrderView(generic.ListView):
  model = md.Order
  template_name = 'dashboard/order/list_all_orders.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = StatusUpdateForm()
    return context
  

class UpdateOrderStatusView(View):

  def post(self, request, *args, **kwargs):
    form = StatusUpdateForm(self.request.POST)
    if form.is_valid():
      md.Order.objects.filter(id=kwargs['pk']).update(status=form.cleaned_data.get('status'))
      messages.success(request, f"Order Status Changed to {form.cleaned_data.get('status')}")
    else:
      messages.error(request, f"Order Status Changed to failed")
      
    return redirect(reverse('dashboard:order_list'))
  
class DetailOrderView(generic.DetailView):
  model = md.Order
  template_name = 'dashboard/order/order_detail.html'
  context_object_name = 'order'
  
class DeleteOrderView(generic.DeleteView):
  success_url = '/orders'
  model = md.Order
  
  
  def get(self, request, *args, **kwargs):
    if self.get_object().delete():
      messages.success(request, 'Order Deleted Successfully')
    return redirect(self.success_url)