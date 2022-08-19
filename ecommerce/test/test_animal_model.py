from django.test import TestCase
from ecommerce import models as m


class TestAnimalModel(TestCase):
  
  def setUp(self) -> None:
    category = m.Category.objects.create(name='Cattle')
    category.save()
    self.category = category
    
    self.animal = m.Animal.objects.create(
      name = 'Red Cross Cattle',
      category = category,
      sex = 'male',
      price = 20.5,
      quantity = 10
    )
    self.animal.save()
    
  def test_animal_created(self):
    self.assertTrue(m.Animal.objects.filter(id = self.animal.id).exists())
    
    
    
    
    