from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class CreateNewUserBaseSerializer(serializers.ModelSerializer):
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)
  role = serializers.SerializerMethodField()
  class Meta:
    abstract = True
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']
    
  def get_role(self, *args):
    return UserProfile.CUSTOMER
  
  def validate(self, attrs):
    if self.get_role() not in ['Customer', "Admin", 'Agent', 'Unknown']:
      raise serializers.ValidationError(_('User Type does not exist'), code='user-type-mismatch')
    return super().validate(attrs)
    
  def create(self, validated_data):
    user = User.objects.create(username=validated_data['username'])
    user.email = validated_data['email']
    user.set_password(validated_data['password'])
    user.is_staff = False
    
    first_name = validated_data.get('first_name', None)
    last_name = validated_data.get('last_name', None)
    
    if first_name: user.first_name = first_name
    if last_name: user.last_name = last_name
    
    if self.get_role() == UserProfile.ADMIN:
      user.is_superuser = True
      user.is_staff = True
      
    elif self.get_role() == UserProfile.AGENT or self.get_role() == UserProfile.CUSTOMER:
      user.is_staff = False
    else:
      pass
  
    
    group, existed = Group.objects.get_or_create(name=self.get_role())
    user.groups.add(group)
    user.save()
    
    profile = UserProfile.objects.create(user_role=self.get_role(), user=user)
    profile.save()
    
    
    validated_data.pop('password')
    return validated_data

class UserProfileSerializers(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user_role',]
  
  
class CreateCustomerUserSerializer(CreateNewUserBaseSerializer):
  
  def get_role(self, *args):
    return UserProfile.CUSTOMER
  
class CreateAdminUserSerializer(CreateNewUserBaseSerializer):
  
  def get_role(self, *args):
    return UserProfile.ADMIN
  
class CreateAgentUserSerializer(CreateNewUserBaseSerializer):
  
  def get_role(self, *args):
    return UserProfile.AGENT
  
  
  
class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()
  
  
  # profile = serializers.SerializerMethodField(read_only=True)
  
  # def get_profile(self, instance):
  #   return instance
    # if self.is_valid():
    #   return None
    
    # profile = UserProfile.objects.filter(user__username=instance.get('username'))
    # return {'user_role': profile.first().user_role}