from django.urls import path, re_path
from .views import *
from rest_framework.schemas import get_schema_view
from account.views.api import AddNewAdminUserAPI, AddNewAgentUserAPI, AddNewCustomerUserAPI, LoginUserAPI, SignOutUserAPI

app_name = 'api'
urlpatterns = [
  path('openapi', get_schema_view(
      title="Animal Ecommerce",
  ), name='openapi-schema'),
  
  path('categorys', listOfCategoryAPI, name='category_list'),
  path('products', ProductListAPI.as_view(), name='product_list'),
  path('customer/owned/products', ProductListByUserAPI.as_view(), name='customer_owned_product_list'),
  path('product/add', ProductAddAPI.as_view(), name='product_add'),
  
  # Auth
  path('auth/register/customer', AddNewCustomerUserAPI.as_view(), name='auth_register_user'),
  path('auth/register/admin', AddNewAdminUserAPI.as_view(), name='auth_register_admin'),
  path('auth/register/agent', AddNewAgentUserAPI.as_view(), name='auth_register_agent'),
  path('auth/login', LoginUserAPI.as_view(), name='sign_in'),
  path('auth/logout', SignOutUserAPI.as_view(), name='sign_out'),
  
  # Order Item
  path('order', OrderAPI.as_view(), name='order'),
  path('orders', OrderListAPI.as_view(), name='list_orders'),
  path('orders/<int:pk>', OrderListAPI.as_view(), name='detail_order'),
  
  
  # Payment
  # path('payments', CreateListPaymentViewAPI.as_view(), name='payment'),
  path('make/payment', PaymentOrderAPI.as_view(), name='make_payment'),
  path('payments', PaymentListAPI.as_view(), name='list_payment'),
  
  path('delivery_points', ListDeliveryPointsAPIView.as_view(), name='delivery_points'),
  
  
  path('product_image', ProductImageCreationAPI.as_view(), name='product_image'),
  
  # # Purchase
  # path('purchase', CreatePurchaseAPI.as_view(), name='purchase'),
  
]
