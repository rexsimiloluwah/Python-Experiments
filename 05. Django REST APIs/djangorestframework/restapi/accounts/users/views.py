from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserDetailSerializer
from api.serializers import PostUserSerializer
from api.models import Posts

User = get_user_model()

class UserDetailAPIView(RetrieveAPIView):
    queryset               = User.objects.filter(is_active = True)
    serializer_class       = UserDetailSerializer
    permission_classes     = [IsAuthenticatedOrReadOnly]
    authentication_classes = []
    lookup_field           = "username"

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}

class PostUserAPIView(ListAPIView):
    serializer_class       = PostUserSerializer
    permission_classes     = []
    authentication_classes = []

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username") or None
        if username is None:
            return Posts.objects.none()

        return Posts.objects.filter(user__username = username)