from django.views import View, generic
import ecommerce.models as md
from django.shortcuts import redirect
from django.contrib import messages

class ListOrderView(generic.ListView):
  model = md.Order
  template_name = 'dashboard/order/list_all_orders.html'
  
  
class DetailOrderView(generic.DetailView):
  model = md.Order
  template_name = 'dashboard/order/order_detail.html'
  
  
class DeleteOrderView(generic.DeleteView):
  success_url = '/orders'
  model = md.Order
  
  
  def get(self, request, *args, **kwargs):
    if self.get_object().delete():
      messages.success(request, 'Order Deleted Successfully')
    return redirect(self.success_url)