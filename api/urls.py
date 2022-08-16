from django.urls import path, re_path
from .views import *
from rest_framework.schemas import get_schema_view


app_name = 'api'
urlpatterns = [
  path('openapi', get_schema_view(
      title="Your Project",
  ), name='openapi-schema'),
  path('categorys', listOfCategoryAPI, name='category_list'),
  path('animals', listAllAnimalsAPI, name='animal_list'),
  
  
  # Order Item
  path('orders', OrderAPI.as_view(), name='order'),
  
  
  # Payment
  path('payments', CreateListPaymentViewAPI.as_view(), name='payment'),
  
  # Purchase
  path('purchase', CreatePurchaseAPI.as_view(), name='purchase'),
]
