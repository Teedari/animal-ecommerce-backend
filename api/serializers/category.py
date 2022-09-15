from rest_framework import serializers
from ecommerce import models as md

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = md.Category
    exclude = ['date_updated',]
    
  