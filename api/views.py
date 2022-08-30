from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import UserProfile
from api.permissions.OnlyCustomPermission import AllowOnlyCustomerPermission
from api.serializers.animal import AnimalSerializer
from api.serializers.category import CategorySerializer
from api.serializers.delivery_point import DeliveryPointSerializer
from api.serializers.order import OrderCreateSerializer
from api.serializers.payment import PaymentCreateSerializer, PaymentListSerializer


from ecommerce.models import Animal, Category, DeliveryPoint, Order, Payment
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
  serializer_class = OrderCreateSerializer
  queryset = Order.objects.all()
  permission_classes = [permissions.IsAuthenticated, AllowOnlyCustomerPermission,]




# class CreateListPaymentViewAPI(generics.ListCreateAPIView):
#   serializer_class = PaymentCreateSerializer
#   queryset = Payment.objects.all()
#   permission_classes = [permissions.IsAuthenticated,]
  
#   def perform_create(self, serializer):
#     serializer.save(paid_by=UserProfile.get_user_profile(self.request.user))
    
class PaymentOrderAPI(generics.CreateAPIView):
  serializer_class = PaymentCreateSerializer
  permission_classes = [permissions.IsAuthenticated,]
  def perform_create(self, serializer):
    serializer.save(paid_by=UserProfile.get_user_profile(self.request.user))
    
class PaymentListAPI(generics.ListAPIView):
  # permission_classes = [ permissions.IsAuthenticated, ]
  serializer_class = PaymentListSerializer
  queryset = Payment.objects.all()

class ListDeliveryPointsAPIView(generics.ListAPIView):
  serializer_class = DeliveryPointSerializer
  queryset = DeliveryPoint.objects.all()
  
  
# class CreatePurchaseAPI(generics.CreateAPIView):
#   serializer_class = PurchaseSerializer