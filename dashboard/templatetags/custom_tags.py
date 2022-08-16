from django import template



register = template.Library()

@register.filter
def choice_value(value):
  print(dir(value))
  
