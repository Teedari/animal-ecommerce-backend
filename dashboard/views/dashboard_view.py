from django.views import generic
from django.contrib.auth import decorators
from django.utils.decorators import method_decorator

from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from account.models import UserProfile

class DashboardHomePageView(UserViewAccessibilityMixin, generic.TemplateView):
  template_name = 'dashboard/index.html'
  # allow_user_profiles = [UserProfile.ADMIN]

  