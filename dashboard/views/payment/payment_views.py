from rest_framework import generics
from django.views import generic
from ecommerce.models import Payment

class ListPaymentView(generic.ListView):
  model = Payment
  template_name = 'dashboard/payments/list_all_payment.html'

