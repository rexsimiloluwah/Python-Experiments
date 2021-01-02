from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username = "similoluwa", email = "rexsimiloluwa@gmail.com")
        user.set_password("terrific")
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username = "similoluwa")
        self.assertEqual(qs.count(), 1)
