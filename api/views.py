from django.shortcuts import render
from rest_framework.views import APIView
# from django.utils.translation import ugettext_lazy as _
from rest_framework import generics
from rest_framework import permissions, response, status, validators
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import UserProfile
from api.permissions.OnlyCustomPermission import AllowOnlyCustomerPermission
from api.serializers.product import ProductCreationSerializer, ProductSerializer
from api.serializers.category import CategorySerializer
from api.serializers.delivery_point import DeliveryPointSerializer
from api.serializers.order import OrderCreateSerializer, OrderSerializer
from api.serializers.payment import PaymentCreateSerializer, PaymentListSerializer
from api.serializers.product_image import ProductImageAddSerializer, ProductImageCreationSerializer


from ecommerce.models import Product, Category, DeliveryPoint, Order, Payment
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
    animal = Product.objects.all()
    serializer = ProductSerializer(animal, many=True)
    return Response(serializer.data)
  
class ProductAddAPI(generics.CreateAPIView):
  serializer_class = ProductCreationSerializer
  permission_classes = [permissions.IsAuthenticated, AllowOnlyCustomerPermission,]
  def perform_create(self, serializer):
    return serializer.save(owner=UserProfile.get_user_profile(self.request.user))
  
  
class ProductListByUserAPI(generics.ListAPIView):
  serializer_class = ProductSerializer
  permission_classes = [permissions.IsAuthenticated, AllowOnlyCustomerPermission,]
  
  def get_queryset(self):
    return Product.objects.filter(owner=UserProfile.get_user_profile(self.request.user))
  
  
class ProductListAPI(generics.ListAPIView):
  serializer_class = ProductSerializer
  
  def get_params(self):
    if 'filter' in self.request.GET.keys():
      queryStr = self.request.GET['filter']
      param_list = [*map(lambda x: x.split(':'), queryStr.split(';'))]
      params = {}
      for param in param_list:
          if len(param) == 2:
            params[param[0]] = param[1]
      return params
  
  def get_queryset(self):
    queryset = Product.objects.all()
    
    queryParams = self.get_params()
    if queryParams:
      try:
        for key in queryParams.keys():
          if key == 'name':
            queryset = queryset.filter(name__istartswith=queryParams[key])
          if key == 'category':
            queryset = queryset.filter(category__id=queryParams[key])
          if key == 'id':
            queryset = queryset.filter(id=queryParams[key])
          if key == 'is_popular' and queryParams[key].lower() == 'yes' or queryParams[key].lower() == 'no':
            queryset = queryset.filter(is_popular=queryParams[key].capitalize())
      except Exception as ex:
        pass
      
    
    return queryset
  

class ProductImageCreationAPI(generics.CreateAPIView):
  serializer_class = ProductImageAddSerializer
class OrderAPI(generics.CreateAPIView):
  serializer_class = OrderCreateSerializer
  queryset = Order.objects.all()
  permission_classes = [permissions.IsAuthenticated, AllowOnlyCustomerPermission,]
  def perform_create(self, serializer):
    serializer.save(customer=UserProfile.get_user_profile(self.request.user))

class OrderListAPI(APIView):
  serializer_class = OrderSerializer
  context = {}
  permission_classes = [permissions.IsAuthenticated, AllowOnlyCustomerPermission,]
  model = Order

  def get_object(self):
    try:
      if 'pk' in self.kwargs:
        self.many = False
        return self.model.objects.get(id=self.kwargs['pk'])
      self.many = True
      return self.model.objects.filter(customer=UserProfile.get_user_profile(self.request.user))
    except self.model.DoesNotExist as ex:
      raise validators.ValidationError((ex), code='does-not-exist')
    
  def serializer(self):
    order = self.get_object()
    _serialize =  OrderSerializer(instance=order, many=self.many)
    self.context = _serialize.data
    
  
  def get(self, request, *args, **kwargs):
    self.serializer()
    return response.Response(data=self.context, status=status.HTTP_200_OK)
  
  # queryset = Order.objects.all()




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
  def get_queryset(self):
    return Payment.objects.filter(paid_by = UserProfile.get_user_profile(self.request.user))

class ListDeliveryPointsAPIView(generics.ListAPIView):
  serializer_class = DeliveryPointSerializer
  queryset = DeliveryPoint.objects.all()
  
  
# class CreatePurchaseAPI(generics.CreateAPIView):
#   serializer_class = PurchaseSerializer