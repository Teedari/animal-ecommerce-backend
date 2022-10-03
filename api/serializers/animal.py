from rest_framework import serializers
from api.serializers.category import CategorySerializer
from ecommerce import models as md


class AnimalSerializer(serializers.ModelSerializer):
  category = serializers.SerializerMethodField()
  class Meta:
    model = md.Product
    exclude = ['date_updated',]
    
  
  def get_category(self, instance):
    return CategorySerializer(instance.category).data


