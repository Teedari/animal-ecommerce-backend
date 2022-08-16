from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import AnimalSerializer, CategorySerializer, OrderSerializer, OrderedItemSerializer, PaymentSerializer, PurchaseSerializer

from ecommerce.models import Animal, Category, Order, Payment
# Create your views here.


@api_view(['GET'])
def listOfCategoryAPI(request):
  if request.method == 'GET':
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
  
@api_view(['GET'])
def listAllAnimalsAPI(request):
  if request.method == 'GET':
    animal = Animal.objects.all()
    serializer = AnimalSerializer(animal, many=True)
    return Response(serializer.data)
  
class OrderAPI(generics.ListCreateAPIView):
  serializer_class = OrderSerializer
  queryset = Order.objects.all()


class CreateListPaymentViewAPI(generics.ListCreateAPIView):
  serializer_class = PaymentSerializer
  queryset = Payment.objects.all()
  
  
class CreatePurchaseAPI(generics.CreateAPIView):
  serializer_class = PurchaseSerializer