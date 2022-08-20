from django.urls import path, re_path
from .views import *
from rest_framework.schemas import get_schema_view
from account.views.api import AddNewAdminUserAPI, AddNewAgentUserAPI, AddNewCustomerUserAPI, LoginUserAPI

app_name = 'api'
urlpatterns = [
  path('openapi', get_schema_view(
      title="Your Project",
  ), name='openapi-schema'),
  
  path('categorys', listOfCategoryAPI, name='category_list'),
  path('animals', listAllAnimalsAPI, name='animal_list'),
  
  # Auth
  path('auth/register/customer', AddNewCustomerUserAPI.as_view(), name='auth_register_user'),
  path('auth/register/admin', AddNewAdminUserAPI.as_view(), name='auth_register_admin'),
  path('auth/register/agent', AddNewAgentUserAPI.as_view(), name='auth_register_agent'),
  path('auth/login', LoginUserAPI.as_view(), name='sign_in'),
  
  # Order Item
  path('orders', OrderAPI.as_view(), name='order'),
  
  
  # Payment
  path('payments', CreateListPaymentViewAPI.as_view(), name='payment'),
  
  # # Purchase
  # path('purchase', CreatePurchaseAPI.as_view(), name='purchase'),
  
]
