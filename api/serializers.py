from dataclasses import field, fields
from math import prod
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ecommerce.models import *
from django.utils.translation import gettext_lazy as _

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    exclude = ['date_updated',]
    
    
class DeliveryPointSerializer(serializers.ModelSerializer):
  class Meta:
    model = DeliveryPoint
    exclude = ['userprofile',]
    
    
class AnimalSerializer(serializers.ModelSerializer):
  category = serializers.SerializerMethodField()
  class Meta:
    model = Animal
    exclude = ['date_updated',]
    
  
  def get_category(self, instance):
    return CategorySerializer(instance.category).data

class OrderItemCreateSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField(write_only=True, required=True)
  class Meta:
    model = OrderedItem
    exclude = ['date_updated',]
    extra_kwargs = {
      'order': {'required': False, 'read_only': True},
      'product': {'required': False, 'read_only': True}
    }
    
  def __init__(self, instance=None, data=..., order=None, **kwargs):
    super().__init__(instance, data, **kwargs)
    if order:
      self.order = order
    
  def validate(self, attrs):
    product = Animal.objects.filter(id=attrs['product_id'])
    if not product:
      raise ValidationError(_('Product is not found in database'), code='product-not-found')
    
    product = product.first()
    
    if product.price != attrs['price']:
      raise ValidationError(_(f"Product #{product.name} price does not match"), code='product-price-does-not-match')
    
    attrs['product'] = product
    
    
      
    return super().validate(attrs)
    
    
  def create(self, validated_data):
    validated_data['order'] = self.order
    return super().create(validated_data)
  
    
class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'
class OrderCreateSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)
  items = OrderItemCreateSerializer(many=True)
  delivery_point_id = serializers.IntegerField(write_only=True)
  # delivery_point = serializers.JSONField(read_only=True)
  total_amount = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=9)
  class Meta:
    model = Order
    fields = '__all__'
    extra_kwargs = {
      "customer": {'required': False},
      "status": {'required': False, 'read_only': True},
    }
    depth = 1
    
  def validate(self, attrs):  
    point = DeliveryPoint.objects.filter(id=attrs.get('delivery_point_id', None))
    if not point.exists():
      raise ValidationError(_('Delivery point cannot be found'))
    self.delivery_point = point.first()
    return super().validate(attrs)
    

  def create(self, validated_data):
    order = None
    try:
      order = Order.objects.create(status=Order.WAITING, delivery_point=self.delivery_point,)
      order.save()
    except Exception as ex:
      raise ValidationError(_('Order create failed try again'))
    
    try:
      items = OrderItemCreateSerializer(data = validated_data['items'], order=order, many=True)
      items.is_valid(raise_exception=True)
      items.save()
    except Exception as ex:
      raise ValidationError(_(ex))   
    
    validated_data['id'] = order.id
    validated_data['total_amount'] = order.total_items_amount
    validated_data['delivery_point'] = self.delivery_point
    validated_data['status'] = order.status
    return validated_data
    

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
  order = OrderCreateSerializer()
  class Meta:
    model = Payment
    exclude = ['date_updated',]
    extra_kwargs = {
      'paid_by': {'read_only': True, 'required': False},
      'remarks': {'read_only': True, 'required': False},
    }
    
    
  def create(self, validated_data):
    order = Order.objects.filter(id = validated_data['order_id'])
    if not order.exists():
      raise serializers.ValidationError(_('Order does not exists'))
    order = order.first()
   
    if not order.is_total_amount_paid_match(validated_data['amount']):
      raise serializers.ValidationError(_(f'Insufficent amount, Try paying the exact amount requested - GH {order.total_items_amount}'), code='insufficent_balance')
    
    validated_data.pop('order_id')

    try:
      payment = Payment.objects.create(**validated_data, order=order)
      payment.is_paid = True
      payment.save()
      validated_data['id'] = payment.id
      order.status = Order.ACCEPTED 
      order.save()
    except Exception as ex:
      raise serializers.ValidationError(_(f'You"ve made payment to #{order.id}'))
    
    return validated_data
  
  
  
  
# class PurchaseSerializer(serializers.Serializer):
#   order = OrderSerializer()
#   payment = PaymentSerializer()
  
  
