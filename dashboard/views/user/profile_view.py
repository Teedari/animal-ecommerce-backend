from django.shortcuts import render
from django.views import View



class UpdateProfile(View):
  context = {}
  template_name = 'dashboard/user/profile.html'
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, self.context)