from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel



class UserProfile(BaseModel):
  UNKNOWN = 'Unknown'
  CUSTOMER = 'Customer'
  ADMIN = 'Admin'
  AGENT = 'Agent' # this could be the delivery driver or the agent
  
  USER_ROLES = (
    (UNKNOWN, UNKNOWN.upper()),
    (CUSTOMER, CUSTOMER.upper()),
    (ADMIN, ADMIN.upper()),
    (AGENT, AGENT.upper()),
  )
  user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='+')
  email_verified = models.BooleanField(default=False)
  user_role = models.CharField(choices=USER_ROLES,default=UNKNOWN, max_length=100)
  
  
  @property
  def is_customer(self):
    return self.user_role == UserProfile.CUSTOMER
  
  @property
  def is_admin(self):
    return self.user_role == UserProfile.ADMIN
  
  @property
  def is_agent(self):
    return self.user_role == UserProfile.AGENT
  
  
  
  @classmethod
  def add_user_to_group(cls, user_role):
    if user_role in list(map(lambda role:  role[0], [])):
      Exception('This user role is not available')
      
  @classmethod 
  def create_user(cls, user, user_role=None):
    if user.is_active and user.is_superuser and user.is_superuser:
      user_role = cls.ADMIN
      
    instance = cls.objects.create(user=user, user_role=user_role)
    instance.save()
    
    return instance
    
    
  @classmethod 
  def get_user_profile(cls, user:'User'):
    profile = cls.objects.filter(user=user)
    return profile.first() if profile.exists() else None
    
    
    
  
  
  