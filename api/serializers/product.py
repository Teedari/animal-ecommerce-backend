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
  # product_images = serializers.ListField(
  #   min_length=2,
  #   child=serializers.ImageField(),
  #   write_only=True
  # )
  # image_1 = serializers.FileField(write_only=True)
  # image_2 = serializers.FileField(write_only=True)
  
  # images = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = md.Product
    # fields = '__all__'
    exclude = ['quantity',]
    
    extra_kwargs = {
      'owner': {'read_only':True, 'required': False}
    }

  def create(self, validated_data):
    product_instance = md.Product.add_new_product(
      name=validated_data.get('name'),
      notes=validated_data.get('notes'),
      weight=validated_data.get('weight'),
      sex=validated_data.get('sex'),
      price=validated_data.get('price'),
      category=validated_data.get('category'),
      owner=validated_data.get('owner')
    )

    # try:
    #   md.ProductImage.create_product_image(product=product_instance, image=validated_data.get('image_1'))
    #   md.ProductImage.create_product_image(product=product_instance, image=validated_data.get('image_2'))
    # except Exception as e:
    #   raise serializers.ValidationError((e))
    
    # instance = ProductImageCreationSerializer(data= validated_data.get('image_1').file, product=product_instance)
    # instance.is_valid(raise_exception=True)
    # instance.save()
    
    
    # data = ProductSerializer(instance=product_instance).data
    # # data.pop('pk')
    # breakpoint()
    # return data
    return product_instance
  
  
  def get_images(self, instance):
    images = instance.product_images.all()
    return ProductImageSerializer(images, many=True).data
    
    
