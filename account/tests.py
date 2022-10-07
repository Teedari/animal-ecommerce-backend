from django.test import Client, TestCase
from django.urls import reverse

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

  def test_should_create_customer(self):
    serializer = CreateCustomerUserSerializer(data=self.dummy_data)
    self.assertTrue(serializer.is_valid())
    serializer.save()
    
    
