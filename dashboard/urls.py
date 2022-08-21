from django.urls import path
from django.views.generic import TemplateView
from dashboard.views.animal.animal_views import AddNewAnimalView, AnimalDeleteView, ListAnimalsView
from dashboard.views.category.category_views import CreateCategory, DeleteCategory, ListCategories
from dashboard.views.dashboard_view import DashboardHomePageView
from dashboard.views.delivery_point.delivery_point_view import CreateDeliveryPoints, EditDeliveryPointView, ListDeliveryPointsView
from dashboard.views.user.list_all_users_view import DeleteUserView, ListUsersView, ToggleUserActiveStatusView
from .views.payment.payment_views import ListPaymentView
from .views.order.order_views import DeleteOrderView, DetailOrderView, ListOrderView
from .views.user.user_admin_creation_view import CreateNewUserAdminView

app_name = 'dashboard'

urlpatterns = [
  path('', DashboardHomePageView.as_view(), name='homepage'),
  
  # User
  path('user/admin/create', CreateNewUserAdminView.as_view(), name='user_create_admin'),
  
  #Category
  path("category", ListCategories.as_view(), name='category_list' ),   
  path("category/<int:pk>/delete", DeleteCategory.as_view(), name='category_delete' ),   
  path("category/create", CreateCategory.as_view(), name='category_add' ), 
  
  # Delivery Point
  path('delivery', ListDeliveryPointsView.as_view(), name='delivery_point_list'),
  path('delivery/create', CreateDeliveryPoints.as_view(), name='delivery_point_add'),
  path('delivery/<int:pk>/edit', EditDeliveryPointView.as_view(), name='delivery_point_edit_detail'),
  
  # Animal
  path('animals', ListAnimalsView.as_view(), name='animal_list'),
  path('animal/add', AddNewAnimalView.as_view(), name='animal_add'),
  path('animal/<int:pk>/delete', AnimalDeleteView.as_view(), name='animal_delete'),
  
  # Order
  path('orders', ListOrderView.as_view(), name='order_list'),
  path('order/<int:pk>', DetailOrderView.as_view(), name='order_detail'),
  path('order/<int:pk>/delete', DeleteOrderView.as_view(), name='order_delete'),
  
  # Payment
  path('payments', ListPaymentView.as_view(), name='payment_list'),
  
  # Users
  path('users', ListUsersView.as_view(), name='user_list'),
  path('user/<int:pk>/delete', DeleteUserView.as_view(), name='user_delete'),
  path('user/<int:pk>/toggle/status', ToggleUserActiveStatusView.as_view(), name='user_toggle_active_status'),
]
