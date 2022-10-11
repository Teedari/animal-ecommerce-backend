from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class CreateNewUserBaseSerializer(serializers.ModelSerializer):
  phone_number = serializers.CharField(max_length=10, write_only=True, required=False)
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)
  role = serializers.SerializerMethodField()
  profile = serializers.SerializerMethodField()
  class Meta:
    abstract = True
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'profile', 'role']
    
    extra_kwargs = {
      'profile': {'read_only': True},
    }
    
  def get_role(self, *args):
    return UserProfile.CUSTOMER
  
  def get_profile(self, instance):
    return UserProfileSerializers(instance=self.profile).data
  
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
    phone_number = validated_data.get('phone_number', None)
    
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
    profile.phone_number = phone_number
    profile.save()
    self.profile = profile
    
    # POP fields
    validated_data.pop('password')
    if phone_number: validated_data.pop('phone_number')
    
    return validated_data
  
  
class UpdateUserProfileInfoSerializer(serializers.ModelSerializer):
  phone_number = serializers.CharField(max_length=10, write_only=True)
  
  class Meta:
    model = User
    fieds = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    
  def validate(self, attrs):
    try:
      
      self.user = User.objects.get(username=attrs.get('username'))
    except User.DoesNotExist as e:
      raise serializers.ValidationError(_(e), code='user-does-not-exist')
    return super().validate(attrs)
  
  def create(self, validated_data):
    phone_number = validated_data.get('phone_number', None)
    profile = UserProfile.objects.filter(user=self.user).update(**validated_data)
    breakpoint()
    if profile == -1:
      raise serializers.ValidationError(_("User Profile Update unsuccessful"))
      

class UserProfileSerializers(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user_role', 'phone_number']

class UserChangePasswordVerificationSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=200)
  email = serializers.CharField(max_length=200)

    
  def validate(self, attrs):
    try:
      self.user = User.objects.get(username=attrs.get('username'), email=attrs.get('email'))
    except User.DoesNotExist as e:
      raise serializers.ValidationError(_('User does not exist in database'), code='user-does-not-exist')
    return super().validate(attrs)
  
  # def save(self, **kwargs):
  #   self.run_validation()
  #   return super().save(**kwargs)
  
  
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