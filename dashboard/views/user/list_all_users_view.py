from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse
from account import models as acc_model
from django.contrib import messages
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin



class ListUsersView(UserViewAccessibilityMixin, generic.ListView):
  allow_user_profiles = [acc_model.UserProfile.ADMIN,]
  template_name = 'dashboard/user/list_all_users.html'
  model = acc_model.UserProfile


class ToggleUserActiveStatusView(UserViewAccessibilityMixin, generic.DetailView):
  allow_user_profiles = [acc_model.UserProfile.ADMIN,]
  template_name =   template_name = 'dashboard/user/list_all_users.html'
  model = acc_model.UserProfile
  context = {}
  
  def get(self, request, *args, **kwargs):
    active = self.get_object().toggle_user_active_status()
    if active:
      messages.success(request, 'User is has permission to access his/her account')
    else:
      messages.warning(request, 'User"s account is disabled')
      
    return redirect(reverse('dashboard:user_list'))
  
class DeleteUserView(generic.DetailView):
  template_name =   template_name = 'dashboard/user/list_all_users.html'
  model = acc_model.UserProfile
  context = {}
  
  def get(self, request, *args, **kwargs):
    self.get_object().user_remove()
    messages.success(request, 'User deleted successfully')
    return redirect(reverse('dashboard:user_list'))