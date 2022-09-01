from django import template

from account.models import UserProfile



register = template.Library()

@register.filter
def choice_value(value):
  print(dir(value))
  
@register.filter
def short_name(value):
  print(value)
  return value.username[0].upper()

@register.filter
def get_currency(value):
  return f'GH₵{value}Gp'
  


# @register.inclusion_tag(name='render_image', filename='components/image_component.html')
# def render_image(**kwargs):
#   print(kwargs)
#   if 'src' in kwargs:
#     return {'src': kwargs['src']}
#   else: 
#     return {'src': 'assets/svgs/undraw_empty.svg', 'default': True}
  
@register.filter
def isAdmin(user):
  profile = UserProfile.objects.filter(user=user)
  return profile.first().user_role == UserProfile.ADMIN
