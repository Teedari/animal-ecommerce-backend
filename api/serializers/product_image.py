from dataclasses import field, fields
from rest_framework import serializers
from ecommerce import models as md

class ProductImageSerializer(serializers.ModelSerializer):
  image = serializers.SerializerMethodField()
  class Meta:
    model = md.ProductImage
    fields = ['image',]
    
  def get_image(self, instance):
    return instance.image.url

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
  
  
  


# NEW
  
  
  
class ProductImageCreateItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = md.ProductImage
    fields = '__all__'
    
  def create(self, validated_data):
    instance = md.ProductImage.create_product_image(product=self.product, image=validated_data.get('image'))
    return instance
  
  
  
class ProductImageAddSerializer(serializers.Serializer):
  image_1 = serializers.FileField()
  # image_2 = serializers.ImageField()
  
  def create(self, validated_data):
    breakpoint()
      # product_image = ProductImageCreateItemSerializer()
    return super().create(validated_data)