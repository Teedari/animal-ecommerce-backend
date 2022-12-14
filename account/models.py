from django.db import models
from django.contrib.auth.models import User

from core.models import BaseModel




class UserProfile(BaseModel):
  UNKNOWN = 'Unknown'
  CUSTOMER = 'Customer'
  ADMIN = 'Admin'
  AGENT = 'Agent' # this could be the delivery driver or the agent
  
  USER_ROLES = (
    # (UNKNOWN, UNKNOWN.upper()),
    # (CUSTOMER, CUSTOMER.upper()),
    (ADMIN, ADMIN.upper()),
    (AGENT, AGENT.upper()),
  )
  user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='+')
  email_verified = models.BooleanField(default=False)
  phone_number = models.CharField(max_length=10, null=True)
  user_role = models.CharField(choices=USER_ROLES, max_length=100)
  
  def __str__(self) -> str:
    return f'{self.user.username} - {self.user_role}'
  
  @property
  def is_customer(self):
    return self.user_role == UserProfile.CUSTOMER
  
  @property
  def is_admin(self):
    return self.user_role == UserProfile.ADMIN
  
  @property
  def is_agent(self):
    return self.user_role == UserProfile.AGENT
  
  @property
  def get_username(self):
    return self.user.get_username()
  
  @property
  def get_phone_number(self):
    return self.phone_number if self.phone_number else 'No contact'
  
  @classmethod
  def add_user_to_group(cls, user_role):
    if user_role in list(map(lambda role:  role[0], [])):
      Exception('This user role is not available')
      
  @classmethod 
  def create_user(cls, user, phone_number=None, user_role=None):
    if user.is_active and user.is_superuser and user.is_superuser:
      user_role = cls.ADMIN
      
    instance = cls.objects.create(user=user, phone_number=phone_number, user_role=user_role)
    instance.save()
    
    return instance
    
    
  @classmethod 
  def get_user_profile(cls, user:'User'):
    profile = cls.objects.filter(user=user)
    return profile.first() if profile.exists() else None
  
  @classmethod
  def get_user_role(cls, user:'User') -> str:
    profile = cls.get_user_profile(user)
    return profile.user_role if profile else None
  
  def toggle_user_active_status(self):
    user = User.objects.filter(id = self.user.id)
    if user:
      user = user.first()
      user.is_active = False if  user.is_active else True
      user.save()
      user.refresh_from_db()
      return user.is_active
    
  def user_remove(self):
    self.user.delete()
    
  def get_assigned_delivery_points(self):
   from ecommerce.models import DeliveryPoint
   return DeliveryPoint.getUserProfileDeliveryPoints(users=[self])

  
  
  
  