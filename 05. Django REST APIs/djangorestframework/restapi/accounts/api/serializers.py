from django.contrib.auth import get_user_model
from rest_framework import serializers 
from django.conf import settings
from django.utils import timezone
import datetime
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .utils import jwt_response_payload_handler

User = get_user_model()

expire_delta = settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"]

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", 
            "username"
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    # Declare fields 
    # Overwrite the model functionality of the password1 and password2 
    password = serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
    # Using a serializer method
    token = serializers.SerializerMethodField(read_only = True)
    expires = serializers.SerializerMethodField(read_only = True)
    message = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "token",
            "expires",
            "message"
        ]
        
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_username(self, value):
        qs = User.objects.filter(username__iexact = value)
        if qs.exists():
            raise serializers.ValidationError(f"User with this username {value} already exists")
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact = value)
        if qs.exists():
            raise serializers.ValidationError(f"User with this email {value} already exists")
        return value

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2") # The password2 is being popped here because we do not need it !
        # print(data)
        if password != password2:
            raise serializers.ValidationError("Passwords do not match !")
        return data

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds = 200)

    def get_message(self, obj):
        return "Thank you for registering, Kindly verify your email before continuing."

    def create(self, validated_data):
        # print(validated_data)

        new_user = User(
            username = validated_data.get("username"),
            email = validated_data.get("email")
        )

        new_user.set_password(validated_data.get("password"))
        new_user.save()
        return new_user
