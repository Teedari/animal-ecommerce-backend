from rest_framework import serializers
from rest_framework.validators import ValidationError
from api.serializers.ordereditem import OrderItemCreateSerializer, OrderedItemSerializer
from ecommerce import models as md

class OrderSerializer(serializers.ModelSerializer):
  items = serializers.SerializerMethodField()
  class Meta:
    model = md.Order
    fields = '__all__'
    depth = 2
    
  def get_items(self, instance):
    return OrderedItemSerializer(instance=instance.ordereditem.all(), many=True).data
class OrderCreateSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)
  items = OrderItemCreateSerializer(many=True)
  delivery_point_id = serializers.IntegerField(write_only=True)
  # delivery_point = serializers.JSONField(read_only=True)
  total_amount = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=9)
  class Meta:
    model = md.Order
    fields = '__all__'
    extra_kwargs = {
      "customer": {'required': False},
      "status": {'required': False, 'read_only': True},
    }
    depth = 1
    
  def validate(self, attrs):  
    point = md.DeliveryPoint.objects.filter(id=attrs.get('delivery_point_id', None))
    if not point.exists():
      raise ValidationError(_('Delivery point cannot be found'))
    self.delivery_point = point.first()
    return super().validate(attrs)
    

  def create(self, validated_data):
    order = None
    try:
      order = md.Order.objects.create(status=md.Order.WAITING, delivery_point=self.delivery_point,)
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
    validated_data['total_amount'] = order.total_amount
    validated_data['delivery_point'] = self.delivery_point
    validated_data['status'] = order.status
    return validated_data
    
