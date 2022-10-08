from rest_framework import serializers
from api.serializers.category import CategorySerializer
from api.serializers.product_image import ProductImageCreationSerializer, ProductImageSerializer
from ecommerce import models as md


class ProductSerializer(serializers.ModelSerializer):
  category = serializers.SerializerMethodField()
  images = serializers.SerializerMethodField()
  class Meta:
    model = md.Product
    exclude = ['date_updated',]
    
  
  def get_category(self, instance):
    return CategorySerializer(instance.category).data
  
  def get_images(self, instance):
   images = instance.product_images.all()
  #  breakpoint()
   return ProductImageSerializer(images, many=True).data



class ProductCreationSerializer(serializers.ModelSerializer):
  product_images = serializers.ListField(
    min_length=2,
    child=serializers.ImageField(),
    write_only=True
  )
  
  images = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = md.Product
    fields = '__all__'
    

  def create(self, validated_data):
    product_instance = md.Product.add_new_product(
      name=validated_data.get('name'),
      notes=validated_data.get('notes'),
      weight=validated_data.get('weight'),
      sex=validated_data.get('sex'),
      price=validated_data.get('price'),
      category=validated_data.get('category'),
    )
    images = list(map(lambda image: {'image': image}, validated_data.get('product_images')))
    instance = ProductImageCreationSerializer(data=images, product=product_instance, many=True)
    instance.is_valid(raise_exception=True)
    instance.save()
    
    
    # data = ProductSerializer(instance=product_instance).data
    # # data.pop('pk')
    # breakpoint()
    # return data
    return product_instance
  
  
  def get_images(self, instance):
    images = instance.product_images.all()
    return ProductImageSerializer(images, many=True).data
    
    
