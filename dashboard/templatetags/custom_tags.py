from django import template



register = template.Library()

@register.filter
def choice_value(value):
  print(dir(value))
  
@register.filter
def short_name(value):
  print(value)
  return value.username[0].upper()