from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import status
from .serializers import TodoSerializer
from .models import Todo
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication

class TodoView(ListAPIView, CreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by("-timestamp")
    permission_classes = []
    authentication_classes = [SessionAuthentication]


class TodoDetailView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by("-timestamp")
    permission_classes = []
    authentication_classes = [SessionAuthentication]

    lookup_field = "id"
