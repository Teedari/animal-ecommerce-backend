from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ecommerce.models import *
from django.utils.translation import gettext_lazy as _

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'
    
    
    
class AnimalSerializer(serializers.ModelSerializer):
  images = serializers.SerializerMethodField()
  category = serializers.SerializerMethodField()
  class Meta:
    model = Animal
    fields = '__all__'
    
  def get_images(self, instance):
    return UploadAnimalImages.objects.filter(animal=instance).values_list('image')
  
  def get_category(self, instance):
    return CategorySerializer(instance.category).data
  
  
  
class OrderedItemSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField(write_only=True)
  product = AnimalSerializer(read_only=True)
  class Meta:
    model = OrderedItem
    fields = ['price', 'quantity', 'product_id', 'product',]
    


    
class OrderSerializer(serializers.ModelSerializer):
  items = OrderedItemSerializer(many=True, required=True, write_only=True)
  ordered_items = OrderedItemSerializer(many=True, read_only=True)
  # ordered_items = serializers.SerializerMethodField(read_only=True)
  id = serializers.IntegerField(read_only=True)
  class Meta:
    model = Order
    fields = ['total_amount', 'items', 'ordered_items', 'id', 'status']
    
    
  def create(self, validated_data):
    order = None
    try:
      order = Order.objects.create(total_amount=validated_data['total_amount'])
      order.save()
    except Exception as err:
      raise serializers.ValidationError('asdfads')
    
    for item in validated_data['items']:
      items = OrderedItem.create_order_item(**item, order=order)
    validated_data['ordered_items'] = [items,]
    return validated_data
  

class PaymentSerializer(serializers.ModelSerializer):
  orderID = serializers.IntegerField(write_only=True)
  order = OrderSerializer(read_only=True)
  class Meta:
    model = Payment
    fields = ['order', 'amount', 'payment_method', 'is_paid', 'remarks', 'orderID']
    
    
  def create(self, validated_data):
    order = Order.objects.filter(id = validated_data['orderID'])
    if not order.exists():
      raise serializers.ValidationError(_('Order does not exists'))
    order = order.first()
    if not order.validate_amount_been_paid(validated_data['amount']):
      raise serializers.ValidationError(_('Insufficent amount, Try paying the exact amount requested'), code='insufficent_balance')
    
    validated_data.pop('orderID')
    payment = Payment.objects.create(**validated_data, order=order)
    payment.is_paid = True
    payment.save()
    return PaymentSerializer(payment).data
  
  
  
  
class PurchaseSerializer(serializers.Serializer):
  order = OrderSerializer()
  payment = PaymentSerializer()
  
  
