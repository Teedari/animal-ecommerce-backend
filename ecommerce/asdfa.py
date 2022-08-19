# from django.test import TestCase
# from django.core.exceptions import ValidationError

# from account.models import UserProfile
# from .models import Animal, Category, Order, OrderedItem, Payment

# from .forms.admin_user_creation_from import CustomUserCreationForm

# # Create your tests here.


# class TestUserCreationForm(TestCase):
  
#   def setUp(self) -> None:
#     self.data = {
#       'username': 'admin',
#       'email': 'admin@gmail.com',
#       'user_role': UserProfile.ADMIN
#     }
#     self.form = CustomUserCreationForm(data=self.data)
    
#   def test_form_validity(self):
#     self.assertTrue(self.form.is_valid())
    
#   def test_has_no_errors(self):
#     self.test_form_validity()
#     self.assertIsNone(self.form.errors if self.form.errors else None)
    
#   def test_user_is_not_unknown(self):
#     self.test_form_validity()
#     self.assertNotEqual(self.form.cleaned_data['user_role'], UserProfile.UNKNOWN)
    
#   def test_save(self):
#     self.test_form_validity()
#     data = self.form.save()
#     self.assertEqual(data['user'].is_active, True)
#     # self.assertDictEqual(self.data, data)
    
#   def test_user_profile_created(self):
#     data = self.form.save()
#     profile = UserProfile.objects.filter(user=data['user'])
#     self.assertTrue(profile.exists())
    
  
# # TEST - MODEL -  ANIMAL  


# class TestAnimalModel(TestCase):
  
#   def setUp(self) -> None:
#     category = Category.objects.create(name='Cattle')
#     category.save()
#     self.category = category
    
#     self.animal = Animal.objects.create(
#       name = 'Red Cross Cattle',
#       category = category,
#       sex = 'male',
#       price = 20.5,
#       quantity = 10
#     )
#     self.animal.save()
    
#   def test_animal_created(self):
#     self.assertTrue(Animal.objects.filter(id = self.animal.id).exists())
    
    
    
# class TestOrderModel(TestCase):
#   def setUp(self) -> None:
#     self.order = Order.objects.create()
#     self.order.save()
    
    
#   def test_order_created(self):
#     print(self.order.total_amount_of_ordered_items)
#     self.assertTrue(Order.objects.filter(id = self.order.id).exists())
    
    
    

# # class TestOrderItemModel(TestAnimalModel, TestOrderModel):
  
# #   def setUp(self) -> None:
# #     TestAnimalModel.setUp(self)
# #     TestOrderModel.setUp(self)
# #     self.orderedItem = OrderedItem.objects.create(product=self.animal, order=self.order, quantity=4)
# #     self.orderedItem.save()
    
# #   # def test_raise_order_quantity_error(self):
# #   #   orderedItem = lambda: OrderedItem.objects.create(product=self.animal, order=self.order, quantity=5)
# #   #   self.assertRaises(ValidationError, orderedItem)
  
# #   def test_order_item_created(self):
# #     self.assertTrue(OrderedItem.objects.filter(id=self.orderedItem.id).exists())
    
# #   def test_order_price_equal_to_product_price(self):
# #     ordered_item = OrderedItem.objects.filter(id=self.orderedItem.id).first()
# #     order_item_price = (ordered_item.item_total_price / ordered_item.quantity) - ordered_item.product.price
# #     self.assertEqual(order_item_price, 0)
    

  
  
# # class TestPaymentModel(TestOrderModel):
  
# #   def setUp(self) -> None:
# #     super().setUp()
# #     self.payment = Payment.objects.create(
# #       payment_method = 'Momo - Paystack',
# #       amount = 10.20,
# #       order = self.order
# #     )
# #     self.payment.save()
  
# #   def test_payment_created(self):
# #     self.assertTrue(Payment.objects.filter(id = self.payment.id).exists())
    