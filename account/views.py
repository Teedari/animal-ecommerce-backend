from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth import logout
from .forms.sign_in_form import SignInForm



class SignInView(View):
  template_name = 'account/sign_in.html'
  form_class = SignInForm
  context = {}
  
  def get(self, request, *args, **kwargs):
    self.context['form'] = self.form_class()
    return render(request, self.template_name, self.context)
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST) 
    if form.is_valid():
      try:
        form.loginUser(request=request)
        return redirect(reverse('dashboard:homepage'))
      except Exception as ex:
        print(ex)
    else:
      self.context['form'] = form
    return render(request, self.template_name, self.context)
  
  
def signOut(request):
  if request.method == 'GET':
    try:
      logout(request)
      return redirect(reverse('account:sign_in'))
    except Exception as err:
      pass
  return redirect(reverse('dashboard:homepage'))
  
    