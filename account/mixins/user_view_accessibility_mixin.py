from django.contrib.auth import decorators, mixins
from django.utils.decorators import method_decorator
from account import models as acc_model

@method_decorator(decorators.login_required, name='dispatch')
class UserViewAccessibilityMixin(mixins.UserPassesTestMixin, mixins.PermissionRequiredMixin):
  allow_user_profiles = []
  def test_func(self):
    if not acc_model.UserProfile.get_user_profile(self.request.user):
      return False
    return acc_model.UserProfile.get_user_role(self.request.user) in self.allow_user_profiles
