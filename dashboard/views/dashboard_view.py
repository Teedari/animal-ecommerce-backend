from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth import decorators
from django.utils.decorators import method_decorator
from django.db.models import Q
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from account.models import UserProfile
from ecommerce.models import Order, Payment

class DashboardHomePageView(UserViewAccessibilityMixin, View):
  template_name = 'dashboard/index.html'
  context = {}
  allow_user_profiles = [UserProfile.ADMIN, UserProfile.AGENT]
  def user(self):
    return UserProfile.get_user_profile(self.request.user)
  def get(self, request, *args, **kwarg):
    if self.user().user_role == UserProfile.AGENT:
      query = Q(delivery_point__userprofile__in=[self.user(),])
      orders = Order.objects.filter(query)
      payments = Payment.objects.filter(order__delivery_point__userprofile__in=[self.user(),])
    else:
      orders = Order.objects.all()
      payments = Payment.objects.all()
      
    # breakpoint()
    
    self.context['order_count'] = orders.count()
    self.context['payment_count'] = payments.count()
    return render(request, self.template_name, self.context)

  