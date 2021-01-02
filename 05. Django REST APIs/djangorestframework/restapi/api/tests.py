from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Posts
from rest_framework import status
from rest_framework.test import APITestCase

class PostTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username = "similoluwa", email = "rexsimiloluwa@gmail.com")
        user.set_password("terrific")
        user.save()

        post_obj = Posts.objects.create(user = user, content = "Hello my people !")

    def test_post(self):
        qs = Posts.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_post_create(self):
        url_login = "http://localhost:8000/api/auth/login"
        details = {
            "username" : "similoluwa", 
            "password" : "terrific"
        }

        response = self.client.post(url_login, details, format = "json")
        # print(response.status_code, response.data)
        token = response.data.get("token")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # self.client.credentials(HTTP_AUTHORIZATION = 'JWT '+token)

        post_url = "http://localhost:8000/api/posts"
        
        data = {
            "content" : "Just trying something out !"
        }

        response2 = self.client.post(post_url, data, format = "json")
        qs = Posts.objects.all()
        print(qs)
        # self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(qs.count(), 2)

