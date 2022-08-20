from decimal import Decimal
from functools import reduce
from typing import Dict
from django.db import models
from core.helpers.funcs import get_readable_choice_value
from core.models import BaseModel
from django.db.models import F, Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class Animal(BaseModel):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=200, blank=True, null=True)
  category = models.ForeignKey(to='Category', related_name='animal_category', on_delete=models.SET_NULL, null=True)
  breed = models.CharField(max_length=200, null=True)
  weight = models.FloatField(max_length=200, null=True)
  sex = models.CharField(choices=(['female', 'Female'], ['male', 'Male']), max_length=10)
  price = models.DecimalField(decimal_places=2, max_digits=999, default=0.00, null=True)
  discount = models.BigIntegerField(null=True)
  quantity = models.BigIntegerField(blank=True, default=0)
  
  
  
  def __str__(self) -> str:
    return f'{self.name} - {self.category} - {self.quantity}'
  

  
class UploadAnimalImages(BaseModel):
  animal =models.ForeignKey(to='Animal', on_delete=models.CASCADE)
  image = models.ImageField(upload_to='media/images/animals')
  
  
  
  def __str__(self) -> str:
    return f'{self.id} - {self.date_created}'
  
  
class Category(BaseModel):
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
  
  
# MODEL-PRODUCT
# class Product(BaseModel):
#   AVAILABLE = 'available'
#   OUT_OF_STOCK = 'out_of_stock'
  
#   STATUS = (
#     (AVAILABLE, AVAILABLE),
#     (OUT_OF_STOCK, get_readable_choice_value(OUT_OF_STOCK))
#   )
  
#   product = models.ForeignKey(to='Animal', on_delete=models.CASCADE)
#   quantity = models.BigIntegerField(default=0)
#   price = models.DecimalField(decimal_places=2, max_digits=999, default=0)
#   discount = models.BigIntegerField(null=True)
#   status = models.CharField(choices=STATUS, default=OUT_OF_STOCK, max_length=100, blank=True)
  
#   @property
#   def jsonfields(self):
#     return {
#       'quantity': self.quantity,
#       'price': self.price,
#       'discount': self.discount
#     }
  
  
  
  
  
# MODEL - Order
class Order(BaseModel):
  WAITING = 'waiting'
  ACCEPTED = 'accepted'
  DECLINED =  'declined'
  DELIVERING = 'delivering'
  RECEIVED = 'received'
  
  ORDERED_STATUS = (
    (WAITING, WAITING),
    (ACCEPTED, ACCEPTED),
    (DECLINED, DECLINED),
    (DELIVERING, DELIVERING),
    (RECEIVED, RECEIVED),
  )

  customer = models.ForeignKey(to='account.UserProfile', null=True, blank=True, related_name='+', on_delete=models.CASCADE)
  status = models.CharField(choices=ORDERED_STATUS, default=WAITING, max_length=100)
  
  
  @property
  def total_items_amount(self):
    total = 0
    for item in  self.ordereditem.all():
      total += item.total_amount
    return total
  
  @property
  def items(self):
    return self.ordereditem.all()
  
  def is_total_amount_paid_match(self, amount):
    if not amount:
      return False
    return self.total_items_amount == amount
  
  
  
  
  
  
class OrderedItem(BaseModel):
  order = models.ForeignKey(to='Order', related_name='ordereditem', on_delete=models.CASCADE)
  product = models.ForeignKey(to='Animal', related_name='+',on_delete=models.DO_NOTHING)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.BigIntegerField(blank=False)
  
  
  
  
  def clean(self):
    from rest_framework.serializers import ValidationError
    if self.quantity > self.product.quantity:
      raise ValidationError(_('Order item quantity exceeds that of the quantity of the product itself'), code='order_quantity_exceed')


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
    product = Animal.objects.filter(id=product_id)

    if product.exists():
      instance = cls.objects.create(**kwargs, product=product.first())
      instance.save()
    return instance
  
    
    
    
    
  
  
class Payment(BaseModel):
  order = models.OneToOneField(to='Order', on_delete=models.CASCADE, null=True)
  amount = models.DecimalField(max_digits=9999, decimal_places=2)
  payment_method = models.CharField(max_length=200)
  is_paid = models.BooleanField(default=False, null=True)
  paid_by = models.ForeignKey(to='account.UserProfile', on_delete=models.CASCADE, null=True)
  status = models.CharField(null=True, max_length=200)
  remarks = models.CharField(null=True, max_length=200)
  
  
  def __str__(self) -> str:
    return '%s - %a' % (self.status, self.amount)

class DeliveryPoint(BaseModel):
  name = models.CharField(max_length=200)
  fee = models.DecimalField(decimal_places=2, max_digits=9999)
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
  
  