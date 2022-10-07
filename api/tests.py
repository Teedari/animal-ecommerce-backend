from django.test import TestCase, Client
from django.urls import reverse
import os
import tempfile
from core.settings import BASE_DIR
from rest_framework import status
from ecommerce.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.



class TestAccountAPI(TestCase):
  def setUp(self) -> None:
    self.client = Client()
    self.dummy_data = {
      'username': 'john_doe',
      'first_name': 'john',
      'last_name': 'doe',
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

class ProductImageAPITest(TestCase):
  def setUp(self) -> None:
    self.client = Client()
    
    
  def test_should_create_product_image(self):
    image = open(os.path.join(BASE_DIR, 'media/test/test.png'), 'rb')
    payload = {
      # 'title': 'how',
      'image': image
    }
    response = self.client.post(reverse('api:product_image'), payload, format='json')
    self.assertEqual(status.HTTP_201_CREATED, response.status_code)

class ProductAPITest(TestCase):
  
  def setUp(self) -> None:
    category = Category.objects.create(name='how')
    category.save()
    self.category = category
    self.image_file = self.get_temp_image_file()
      
  
  def get_temp_image_file(self):
    try:
      image = open(os.path.join(BASE_DIR, 'media/test/product_test_image.png'), 'rb')
    except FileNotFoundError:
      image = open(os.path.join(BASE_DIR, 'media/test/product_test_image.png'), 'wb')
    return image
    
    
  def test_should_add_new_product(self):
    image = open(os.path.join(BASE_DIR, 'media/test/test.png'), 'rb')
    image2 = open(os.path.join(BASE_DIR, 'media/test/test.png'), 'rb')
    # with open(os.path.join(BASE_DIR, 'media/test/test.png'), 'rb') as fp:
    # file = SimpleUploadedFile('test_image.png', b'file_content', content_type='image/png')
    # print(file)
    payload = {
   
    "product_images": [image, image2],

    "name": "string",
    "notes": "string",
    "weight": 0,
    "sex": "female",
    "price": 887,
    "quantity": 0,
    "is_popular": "No",
    # "images": 'asdjfalks'
  }
  
    
    response = Client().post(reverse('api:product_add'), payload)
    self.assertEqual(201, response.status_code)