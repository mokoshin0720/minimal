from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.utils import timezone
from minimal.models import CustomUser

class UserModelTests(TestCase):
    def setUp(self):
        CustomUser.objects.create(username="test", password="testpass")
        
    def test_user_count(self):
        saved_user = CustomUser.objects.all()
        self.assertEqual(saved_user.count(), 1)

    def test_user_create(self):
        user = CustomUser.objects.get(username="test")
        self.assertEqual(user.password, "testpass")