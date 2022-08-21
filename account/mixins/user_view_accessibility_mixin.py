from django.contrib.auth import mixins
from django.utils.decorators import method_decorator
from account import models as acc_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
  
  
class UserViewAccessibilityMixin(mixins.UserPassesTestMixin):
  allow_user_profiles = []
  def test_func(self):
    if not acc_model.UserProfile.get_user_profile(self.request.user):
      return False
    return acc_model.UserProfile.get_user_role(self.request.user) in self.allow_user_profiles
  
  
  def dispatch(self, request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated or user.is_anonymous:
      return redirect(reverse('account:sign_in'))
    return super().dispatch(request, *args, **kwargs)
  
