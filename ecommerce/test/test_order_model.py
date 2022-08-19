from http import client
from django.test import TestCase
from django.test.client import Client
from ecommerce import models as m
from django.contrib.auth.models import User

from django.contrib.auth import get_user
 
 

class TestOrderModel(TestCase):
  def setUp(self) -> None:
    self.order = m.Order.objects.create()
    self.order.save()
    
    
  def test_order_created(self):
    self.assertTrue(m.Order.objects.filter(id = self.order.id).exists())
    