from rest_framework import serializers
from rest_framework.validators import ValidationError
from api.serializers.product import ProductSerializer
from ecommerce import models as md


class OrderedItemSerializer(serializers.ModelSerializer):
  product = serializers.SerializerMethodField()
  class Meta:
    model = md.OrderedItem
    fields ='__all__'
    
  def get_product(self, instance):
    return ProductSerializer(instance=instance.product).data
  
class OrderItemCreateSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField(write_only=True, required=True)
  class Meta:
    model = md.OrderedItem
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
    product = md.Animal.objects.filter(id=attrs['product_id'])
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
  
    
