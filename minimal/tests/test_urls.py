from django.test import TestCase
from django.urls import reverse, resolve
from minimal.views import index

class TestUrls(TestCase):
    def test_post_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)