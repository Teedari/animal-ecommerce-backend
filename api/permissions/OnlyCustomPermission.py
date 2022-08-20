from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from account.models import UserProfile


class AllowOnlyCustomerPermission(BasePermission):
  
  def has_permission(self, request, view):
    profile = UserProfile.get_user_profile(request.user)
    if not profile:
      raise PermissionDenied(_('User must have a profile'), code='no-user-profile')
    if profile.user_role != UserProfile.CUSTOMER:
      raise PermissionDenied(_('Access denied, You need to be a customer to perform such action'), code='user-access-denied')
    return super().has_permission(request, view)