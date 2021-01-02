from django.test import TestCase

from rest_framework.test import APITestCase  # This is the module that will be used for testing in rest_framework
from rest_framework import status
# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

from api.models import Posts

class UsersTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username = "similoluwa", email = "rexsimiloluwa@gmail.com")
        user.set_password("terrific")
        user.save()

    def test_user_std(self):
        qs = User.objects.filter(username = "similoluwa")
        self.assertEqual(qs.count(), 1)

    def test_user_register(self):
        url = "http://localhost:8000/api/auth/register"
        data = {
            "username" : "davido",
            "email"    : "davido@gmail.com",
            "password" : "terrific", 
            "password2" : "terrific"
        }

        response = self.client.post(url, data, format = "json")
        # Response status code 
        status_code = response.status_code
        print(status_code)
        print(response.data)
        self.assertEqual(status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = "http://localhost:8000/api/auth/login"
        data = {
            "username" : "similoluwa", 
            "password" : "terrific"
        }

        response = self.client.post(url, data, format = "json")
        # Geting the token
        token = response.data.get("token", 0)
        print(token)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertGreater(token_len, 0)
        # Response status code 
        status_code = response.status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

        # Testing login with a logged in client's credentials 
        self.client.credentials(HTTP_AUTHORIZATION = "JWT "+ token)
        response2 = self.client.post(url, data, format = "json")
        print("Response 2 status code", response2.status_code)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)