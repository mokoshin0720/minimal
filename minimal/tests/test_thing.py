from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.utils import timezone
from minimal.models import CustomUser, MinimalModel, ThingStatus

class ThingModelTests(TestCase):


    def setUp(self):
        CustomUser.objects.create(username="test", password="testpass")
        ThingStatus.objects.create(name="満足")
        MinimalModel.objects.create(title="冷蔵庫",
                                    author=CustomUser.objects.get(username="test"),
                                    status=ThingStatus.objects.get(name="満足"),
                                    buy_reason="保存するため",
                                    buy_date=timezone.now(),
                                    buy_price=100)

    def test_thing_count(self):
        saved_user = MinimalModel.objects.all()
        self.assertEqual(saved_user.count(), 1)

    def test_user_create(self):
        thing = MinimalModel.objects.get(title="冷蔵庫")
        self.assertEqual(thing.buy_price, 100)