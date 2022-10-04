from dataclasses import field
from rest_framework import serializers
from ecommerce import models as md




class ProductImageCreationSerializer(serializers.ModelSerializer):
  # title = serializers.CharField(write_only=True)
  class Meta:
    model = md.ProductImage
    fields = '__all__'
    
    extra_kwargs ={
      'product': {'required': False}
    }
    
  def __init__(self, instance=None, data=..., product=None, **kwargs):
    super().__init__(instance, data, **kwargs)
    self.product = product
    
  def create(self, validated_data):
    instance = md.ProductImage.create_product_image(product=self.product, image=validated_data.get('image'))
    return instance