from account.serializers import  CreateAdminUserSerializer, CreateAgentUserSerializer, CreateCustomerUserSerializer, UserLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, response, exceptions, status
from django.contrib.auth import authenticate, logout
from utils.generators.rest_framework_jwt_token_generator import get_tokens_for_user
from django.utils.translation import gettext_lazy as _
### API ACCOUNT SECTION



class AddNewCustomerUserAPI(CreateAPIView):
  serializer_class = CreateCustomerUserSerializer
class AddNewAdminUserAPI(CreateAPIView):
  serializer_class = CreateAdminUserSerializer
class AddNewAgentUserAPI(CreateAPIView):
  serializer_class = CreateAgentUserSerializer
  
 
class LoginUserAPI(APIView):
  permission_classes = [permissions.AllowAny,]
  def post(self, request):
    try:
      serializer = UserLoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      # breakpoint()
      auth = authenticate(request, username = serializer.data.get('username', None), password=serializer.data.get('password', None))
      if not auth:
        raise exceptions.AuthenticationFailed('Invalid Credentials')

      user = UserLoginSerializer(instance=serializer.data).data
      user.pop('password')
      data = {
        'user': user,
        **get_tokens_for_user(auth)
      }
      return response.Response(data=data, status=status.HTTP_200_OK)
    except Exception as ex:
      raise ex

class SignOutUserAPI(APIView):
  def get(self,request, *args, **kwargs):
    try:
      logout(request)
    except Exception as ex:
      raise exceptions.ValidationError(_('Unexpected error occuried, please try again'), 'sign-out-error')
    return response.Response({
      'token': None,
      'user': None
    }, status=status.HTTP_200_OK)
    