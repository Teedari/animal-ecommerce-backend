from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from account.mixins.user_view_accessibility_mixin import UserViewAccessibilityMixin
from ecommerce.forms.profile_forms import ProfileUserInfoUpdateForm, ProfileUserPasswordChangeForm
from django.contrib import messages



class UpdateProfile(View):
  context = {}
  template_name = 'dashboard/user/profile.html'
  form_class = ProfileUserInfoUpdateForm
  # is_admin_only = True
  
  def get_object(self):
    user = get_user(self.request)
    return {
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
    }
  
  def get(self, request, *args, **kwargs):
    self.context['user_pass_form'] = ProfileUserPasswordChangeForm()
    self.context['user_info_form'] = self.form_class(self.get_object())
    return render(request, self.template_name, self.context)
  
  
class ProfileUpdateBase(generic.UpdateView):
  model = User
  success_url = '/user/profile'
  template_name = 'dashboard/user/profile.html'
  class Meta:
    abstract = True
    
    
    
  def get_context_data(self, **kwargs):
    user = get_user(self.request)
    user = {
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
    }
    context = super().get_context_data(**kwargs)
    context['user_pass_form'] = ProfileUserPasswordChangeForm()
    context['user_info_form'] = ProfileUserInfoUpdateForm(user)
    return context
class UpdateUserProfileDetails(ProfileUpdateBase):
  form_class = ProfileUserInfoUpdateForm

  def post(self, request, *args, **kwargs):
    messages.success(request, 'User Information Updated Successfully')
    return super().post(request, *args, **kwargs)
  
  
class UpdateUserProfilePassword(generic.FormView):
  form_class = ProfileUserPasswordChangeForm
  success_url = '/user/profile'
  template_name = 'dashboard/user/profile.html'
  _is_password_change = False
  def form_valid(self, form):
    form.change_password(self.request.user)
    self._is_password_change = True
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = get_user(self.request)
    user = {
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
    }
    context['user_pass_form'] = ProfileUserPasswordChangeForm()
    context['user_info_form'] = ProfileUserInfoUpdateForm(user)
    return context
  
  
  def post(self, request, *args, **kwargs):
    form = self.get_form()
    if form.is_valid():
      form.change_password(self.request.user)
      self._is_password_change = True
      messages.success(request, 'Password changed successfully')
      return redirect(reverse('account:sign_out'))
    else:
      error = tuple(self.get_form().errors.values())[0][0]
      messages.error(request, f'{error}')

    return super().post(request, *args, **kwargs)
  