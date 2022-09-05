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
  order = OrderCreateSerializer(write_only=True)
  id = serializers.IntegerField(read_only=True)
  class Meta:
    model = md.Payment
    exclude = ['date_updated',]
    extra_kwargs = {
      'paid_by': {'read_only': True, 'required': False},
      'remarks': {'read_only': True, 'required': False},
    }
    ordering = ['-date_created']
    
  def create(self, validated_data):
    
    order = OrderCreateSerializer(data=validated_data.get('order'))
    order.is_valid(raise_exception=True)
    order.save()
    order = order.data
    # breakpoint()
    if  float(order.get('total_amount')) < float(validated_data.get('amount')):
      md.Order.objects.filter(id=order.get('id')).delete()
      raise serializers.ValidationError(_(f'Insufficent amount, Try paying the exact amount requested - GHc { order.get("total_amount") }'), code='insufficent_balance')
    elif  float(order.get('total_amount')) > float(validated_data.get('amount')):
      md.Order.objects.filter(id=order.get('id')).delete()
      raise serializers.ValidationError(_(f'Amount is more, Try paying the exact amount requested - GHc { order.get("total_amount") }'), code='amount_exceed')
    
    

    try:
      validated_data.pop('order')
      payment = md.Payment.objects.create(**validated_data, order=md.Order.objects.filter(id=order.get('id')).first())
      payment.is_paid = True
      payment.save()
      validated_data['id'] = payment.id
      md.Order.objects.filter(id=order.get('id')).update(status=md.Order.ACCEPTED, customer=validated_data.get('paid_by', None))
    except Exception as ex:
      raise serializers.ValidationError(_(f'Payment of order #{order.get("id")} was unsuccessful'))
    o = OrderCreateSerializer(instance=md.Order.objects.filter(id=order.get('id')).first())
    # o.is_valid(raise_exception=True)
    # validated_data['order'] = o.validated_data
    validated_data['order'] = o.data
    dd = PaymentCreateSerializer(instance=validated_data)
    return validated_data
  
  
  
  