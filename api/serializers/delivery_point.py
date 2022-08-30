from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ecommerce import models as md 

class DeliveryPointSerializer(serializers.ModelSerializer):
  class Meta:
    model = md.DeliveryPoint
    exclude = ['userprofile',]
    
    
