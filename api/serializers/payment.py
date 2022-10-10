from rest_framework import serializers
from api.serializers.ordereditem import OrderedItemSerializer
from ecommerce import models as md


from api.serializers.order import OrderCreateSerializer, OrderSerializer


class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = md.Payment
    fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):
  order = serializers.SerializerMethodField()
  class Meta:
    model = md.Payment
    fields = '__all__'
    depth = 1
  
  def get_order(self, instance):
    # ordereditems = instance.order.ordereditem.all()
    return OrderSerializer(instance=instance.order).data

class PaymentCreateSerializer(serializers.ModelSerializer):
  order_id = serializers.IntegerField(write_only=True)
  class Meta:
    model = md.Payment
    exclude = ['date_updated',]
    extra_kwargs = {
      'order': {'read_only': True, 'required': False},
      'paid_by': {'read_only': True, 'required': False},
      'remarks': {'read_only': True, 'required': False},
    }
    ordering = ['-date_created']
    
  def validate(self, attrs):
    if 'amount' not in attrs.keys():
      raise serializers.ValidationError(('Amount field required'))
    try:
       self.order = md.Order.objects.get(id=attrs.get('order_id'))
    except md.Order.DoesNotExist as ex:
      raise serializers.ValidationError((ex))
    if  float(self.order.total_amount) < float(attrs.get('amount')):
      raise serializers.ValidationError((f'Insufficent amount, Try paying the exact amount requested - GHc { self.order.total_amount }'), code='insufficent_balance')
    elif  float(self.order.total_amount) > float(attrs.get('amount')):
      raise serializers.ValidationError((f'Amount is more, Try paying the exact amount requested - GHc { self.order.total_amount }'), code='amount_exceed')
    return super().validate(attrs)
    
  def create(self, validated_data):
    order = OrderCreateSerializer(instance=self.order).data

    try:
      payment = md.Payment.objects.create(**validated_data, order=md.Order.objects.filter(id=order.get('id')).first())
      payment.is_paid = True
      payment.save()
      validated_data['id'] = payment.id
      md.Order.objects.filter(id=order.get('id')).update(status=md.Order.DELIVERING, customer=validated_data.get('paid_by', None))
    except Exception as ex:
      raise serializers.ValidationError((f'Payment of order #{order.get("id")} was unsuccessful'))
    return payment
  
  
  
  