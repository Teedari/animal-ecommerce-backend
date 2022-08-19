from django.test import TestCase
from account.models import UserProfile
from ecommerce.forms.admin_user_creation_from import CustomUserCreationForm

class TestUserCreationForm(TestCase):
  
  def setUp(self) -> None:
    self.data = {
      'username': 'admin2',
      'email': 'admin@gmail.com',
      'user_role': UserProfile.ADMIN
    }
    self.form = CustomUserCreationForm(data=self.data)
    
  def test_form_validity(self):
    self.assertTrue(self.form.is_valid())
    
  def test_has_no_errors(self):
    self.test_form_validity()
    self.assertIsNone(self.form.errors if self.form.errors else None)
    
  def test_user_is_not_unknown(self):
    self.test_form_validity()
    self.assertNotEqual(self.form.cleaned_data['user_role'], UserProfile.UNKNOWN)
    
  def test_save(self):
    self.test_form_validity()
    data = self.form.save()
    self.assertEqual(data['user'].is_active, True)
    # self.assertDictEqual(self.data, data)
    
  def test_user_profile_created(self):
    self.test_form_validity()
    data = self.form.save()
    profile = UserProfile.objects.filter(user=data['user'])
    self.assertTrue(profile.exists())
  