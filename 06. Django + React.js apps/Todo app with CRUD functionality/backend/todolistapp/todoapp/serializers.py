from rest_framework import serializers
from .models import Todo

from django.contrib.auth import get_user_model 
User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

class TodoSerializer(serializers.ModelSerializer):

    user = UserPublicSerializer(read_only = True)
    class Meta:
        model = Todo

        fields = '__all__'

