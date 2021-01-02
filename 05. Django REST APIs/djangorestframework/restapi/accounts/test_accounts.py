from django.test import TestCase

from rest_framework.test import APITestCase  # This is the module that will be used for testing in rest_framework

# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

from api.models import Posts

class AccountsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username = "similoluwa", email = "rexsimiloluwa@gmail.com")
        user.set_password("terrific")
        user.save()

    def test_demo(self):
        self.assertEqual(2, (5/2.5))