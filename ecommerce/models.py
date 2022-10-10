from decimal import Decimal
import decimal
from functools import reduce
from typing import Dict
from django.db import models
from core.helpers.funcs import get_readable_choice_value
from core.models import BaseModel
from django.db.models import F, Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField






class Product(BaseModel):
  name = models.CharField(max_length=200)
  notes = models.CharField(max_length=200, blank=True, null=True)
  category = models.ForeignKey(to='Category', related_name='product_category', on_delete=models.SET_NULL, null=True)
  weight = models.FloatField(max_length=200, null=True)
  sex = models.CharField(choices=(['female', 'Female'], ['male', 'Male']), max_length=10)
  price = models.DecimalField(decimal_places=2, max_digits=1000, default=0.00, null=True)
  quantity = models.BigIntegerField(blank=True, default=0)
  is_popular = models.CharField(choices=[ ('No', False), ('Yes', True)], max_length=10, default=False)
  owner = models.ForeignKey(to='account.UserProfile', null=True, related_name='product_owner', on_delete=models.CASCADE)
  
  
  def __str__(self) -> str:
    return f'{self.name} - {self.category} - {self.is_popular}'
  
  
  @classmethod
  def add_new_product(cls, name:str, notes:str, category:str, weight:float, sex:str, price:decimal):
    instance = cls.objects.create(name=name, sex=sex, weight=weight, price=price, category=category)
    instance.notes = notes if notes else ''
    instance.save()
    return instance
  
class ProductImage(BaseModel):
  product = models.ForeignKey(to='Product', related_name='product_images', on_delete=models.CASCADE, null=True)
  image = CloudinaryField()
  
  def __str__(self):
    return f'{self.id} | {self.product.name}'
  
  
  @classmethod
  def create_product_image(cls, product, image):
    obj = cls.objects.create(product=product, image=image)
    obj.save()
    return obj
    
  @classmethod
  def get_product_images_by_product(cls, product):
    instances = cls.objects.filter(product=product)
    return instances if instances.exists() else None


  
  
class Category(BaseModel):
  # POULTRY = 'Poultry'
  # CATTLE = 'Cattle'
  # SHEEP =  'Sheep'
  # GOAT =  'Goat'
  # SWINE =  'Swine'
  # NONE = ""
  
  # Product_CHOICES = (
  #   (NONE, "Classes of Products"),
  #   (POULTRY, POULTRY),
  #   (CATTLE, CATTLE),
  #   (SHEEP, SHEEP),
  #   (GOAT, GOAT),
  #   (SWINE, SWINE),
  # )
  name = models.CharField(max_length=200, unique=True)
  description = models.TextField(blank=True, null=True)
  
  def __str__(self):
    return f'{self.id} - {self.name}'
  
  @classmethod
  def remove(cls, id:int) -> bool:
    category = cls.objects.filter(id=id)
    if category.exists():
      category.first().delete()
      return True
  
   
# MODEL - Order
class Order(BaseModel):
  WAITING = 'waiting'
  # ACCEPTED = 'accepted'
  # DECLINED =  'declined'
  DELIVERING = 'delivering'
  RECEIVED = 'received'
  
  ORDERED_STATUS = (
    ('', 'Select'),
    (WAITING, WAITING),
    # (ACCEPTED, ACCEPTED),
    # (DECLINED, DECLINED),
    (DELIVERING, DELIVERING),
    (RECEIVED, RECEIVED),
  )

  customer = models.ForeignKey(to='account.UserProfile', null=True, blank=True, related_name='+', on_delete=models.CASCADE)
  delivery_point = models.ForeignKey(to='DeliveryPoint', null=True, blank=True, related_name='+', on_delete=models.DO_NOTHING)
  status = models.CharField(choices=ORDERED_STATUS, default=WAITING, max_length=100)
  
  
  
  
  
  @property
  def total_items_amount(self):
    total = 0
    for item in  self.ordereditem.all():
      total += item.total_amount
    return total
  
  @property
  def total_amount(self):
    return self.total_items_amount + self.delivery_point.fee
  
  @property
  def items(self):
    return self.ordereditem.all()
  
  
  @property 
  def items_in_cart(self):
    return sum([ quantity[0] for quantity in self.items.values_list('quantity')])
  
  @property
  def payment(self):
    return self.payment_order
  
  def is_accepted(self):
    try:
      return self.payment_order
    except Exception as e:
      return None
  
  def is_waiting(self):
    return self.status == Order.WAITING
  
  def is_delivering(self):
    return self.status == Order.DELIVERING
  
  def is_received(self):
    return self.status == Order.RECEIVED
  
  def is_total_amount_paid_match(self, amount):
    if not amount:
      return False
    return self.total_amount == amount
  
  # def get_payments_history(self):
  #   return self.payment_order
  
  
  
  
  
  
class OrderedItem(BaseModel):
  order = models.ForeignKey(to='Order', related_name='ordereditem', on_delete=models.CASCADE)
  product = models.ForeignKey(to='Product', related_name='+',on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=1000, decimal_places=2)
  quantity = models.BigIntegerField(blank=False)
  
  
  
  
  # def clean(self):
  #   from rest_framework.serializers import ValidationError
  #   if self.quantity > self.product.quantity:
  #     raise ValidationError(_('Order item quantity exceeds that of the quantity of the product itself'), code='order_quantity_exceed')


  def save(self, *args, **kwargs) -> None:
    self.full_clean()
    self.price = self.product.price
    return super().save(*args, **kwargs)
  
  
  @property
  def total_amount(self):
    return self.price * self.quantity
  
  @classmethod
  def create_order_item(cls, **kwargs):
    instance = None
    product_id = kwargs['product_id']
    kwargs.pop('product_id')
    product = Product.objects.filter(id=product_id)

    if product.exists():
      instance = cls.objects.create(**kwargs, product=product.first())
      instance.save()
    return instance

  def product_info(self):
    info = {}
    info['']
    
    
    
    
  
  
class Payment(BaseModel):
  order = models.OneToOneField(to='Order', related_name='payment_order', on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=100,)
  phone_number = models.CharField(max_length=10)
  amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
  payment_method = models.CharField(max_length=200)
  is_paid = models.BooleanField(default=False, null=True)
  paid_by = models.ForeignKey(to='account.UserProfile', on_delete=models.CASCADE, null=True)
  status = models.CharField(null=True, max_length=200)
  remarks = models.CharField(null=True, max_length=200)
  
  
  def __str__(self) -> str:
    return '%s - %a' % (self.status, self.amount)

class DeliveryPoint(BaseModel):
  name = models.CharField(max_length=200)
  fee = models.DecimalField(decimal_places=2, max_digits=1000)
  description = models.CharField(max_length=200, null=True, blank=True)
  userprofile = models.ManyToManyField('account.UserProfile')
  
  def __str__(self) -> str:
    return f"{self.name} - {self.fee}"
  
  @property
  def get_serialized_form_data(self) -> Dict:
    return {
      'name': self.name,
      'fee': self.fee,
      'description': self.description
    }
  
  