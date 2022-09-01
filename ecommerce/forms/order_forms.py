from random import choices
from django import forms
from ecommerce.models import Order

class StatusUpdateForm(forms.Form):
  status = forms.ChoiceField(choices=Order.ORDERED_STATUS)