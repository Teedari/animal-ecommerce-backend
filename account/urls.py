from django.urls import path

from account.views.view import SignInView, signOut




app_name = 'account'


urlpatterns = [
  path('', SignInView.as_view(), name='sign_in'),
  path('sign-out', signOut, name='sign_out')
]