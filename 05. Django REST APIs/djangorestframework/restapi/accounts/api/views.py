from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q # This is only a lookup method
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer
from accounts.permissions import AnonPermissionOnly

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .utils import jwt_response_payload_handler

User = get_user_model()

class AuthAPIView(APIView):
    authentication_classes = []
    permission_classes = [AnonPermissionOnly]
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail" : "You are already authenticated Bro. !"}, status = 400)
        
        # Authenticating an anonymous user 
        data = request.data
        username = data.get("username")
        password = data.get("password")
        # user = authenticate(username = username, password = password)
        # To complete the authentication or verification of the user's authenticity
        queryset = User.objects.filter(
            Q(username__iexact = username) |
            Q(email__iexact = username)
        )


        if queryset.count() == 1:
            user_obj = queryset.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request = request)
                print(user)
                return Response(response)

        return Response({"detail" : "Invalid Credentials"}, status = 400)


class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
            desc : This is the POST method for the function that is used to register a user
        """
        if request.user.is_authenticated:
            return Response({"detail" : "User is already authenticated and Registered !"}, status = 400)
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            return Response({"detail" : "Passwords do not match !"}, status = 400)

        # To check if the user exists 
        queryset = User.objects.filter(
            Q(username__iexact = username) |
            Q(email__iexact = username)
        )

        if queryset.exists():
            return Response({"detail" : f"This User with E-mail {email} already exists !"}, status = 400)
        else:
            user = User.objects.create(username = username, password = password)
            user.set_password = password
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token, user, request = request)
            print(user)
            return Response(response, status = 201)

        return Response({"detail" : "Invalid Request !"}, status = 400)


class RegisterAPIViewSerialized(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [AnonPermissionOnly]
