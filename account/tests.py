from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from account.serializers import CreateCustomerUserSerializer

# Create your tests here.


class TestCreateCustomerUserSerializer(TestCase):
  def setUp(self) -> None:
    self.dummy_data = {
      'username': 'test_username',
      'first_name': 'test_first_name',
      'last_name': 'test_last_name',
      'email': 'test_email@gmail.com',
      'password': 'test_password',
    }
    self.client = Client()

  def test_should_create_customer_with_no_phone_number(self):
    serializer = CreateCustomerUserSerializer(data=self.dummy_data)
    self.assertTrue(serializer.is_valid())
    serializer.save()
    
  def test_should_create_customer_with_phone_number(self):
    data = {**self.dummy_data, 'phone_number': '0247123456'}
    
    serializer = CreateCustomerUserSerializer(data=data)
    self.assertTrue(serializer.is_valid())
    instance = serializer.save()
 
 
#  def test_should_create_customer_api(self):
#    response = self.client(reverse(''))

    
  
  
  
    
class TestAccountAPI(TestCase):
  def setUp(self) -> None:
    self.client = Client()
    self.dummy_data = {
      'username': 'john_doe',
      'first_name': 'john',
      'last_name': 'doe',
      'phone_number': '0247123456',
      'email': 'doe@test.com',
      'password': 'doe12345'
    }
    
  def test_should_register_customer(self):
    response = self.client.post(reverse('api:auth_register_user'), self.dummy_data)
    self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    
  def test_should_signin_customer(self):
    self.test_should_register_customer()
    data = {
      'username': self.dummy_data['username'],
      'password': self.dummy_data['password']
    }
  
    response = self.client.post(reverse('api:sign_in'), data, format='json')
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    print(response.json())
    
  def test_should_verify_users_existence_failed(self):
    self.test_should_register_customer()
    data = {
      'username': 'asdjflkdsf',
      'email': 'sdlj@gmail.com',
    }
    response = self.client.post(reverse('api:auth_user_verify_existence'), data=data)
    self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
  def test_should_verify_users_existence(self):
    self.test_should_register_customer()
    data = {
      'username': self.dummy_data['username'],
      'email': self.dummy_data['email'],
    }
    response = self.client.post(reverse('api:auth_user_verify_existence'), data=data)
    self.assertEqual(status.HTTP_200_OK, response.status_code)
