from django.shortcuts import render

## Required rest framework packages for the API Views
from rest_framework.views import APIView
from rest_framework.response import Response 
# Generic View Instances
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
# Model Mixins
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
# For Authentication and Permission purposes 
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from accounts.permissions import IsOwnerOrReadOnly

from .models import Posts
from .serializers import PostSerializer
import json
from django.shortcuts import get_object_or_404

def is_json(data):
    try:
        json_data = json.loads(data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid



# Create your views here.

# @desc --> List and Search View , @methods --> GET
class PostListAndSearchView(APIView):
    # permission_classes = []
    # authentication_classes = []

    # GET METHOD 
    def get(self, request, format = None, *args, **kwargs):
        qs = Posts.objects.all()
        serialized_data = PostSerializer(qs, many = True)
        return Response(serialized_data.data)

# @desc --> Easier way of working with the View
class PostSearchView(CreateModelMixin, ListAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly] 
    # authentication_classes = [SessionAuthentication] # Other authentication methods are JWT, and Oauth
    serializer_class = PostSerializer
    search_fields = ("user__username", "content")
    def get_queryset(self):
        qs = Posts.objects.all()
        # print(self.request.user)
        query = self.request.GET.get("q")
        if query  is not None:
            qs = qs.filter(content__icontains = query)

        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Performing create method constraints 
    def perform_create(self, serializer): # This will ensure that the user currently logged in the session will be automatically saved with the post data
        serializer.save(user = self.request.user)

    
        
# @desc --> Create API View (for the Create method), @methods --> POST
class PostCreateView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # Other methods 

class PostDetailView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = []
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # To utilize the UpdateModelMixin
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # To utilize the DestroyModelMixin
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    


# @desc --> Update API View for the PUT Method, @methods --> PUT
class PostUpdateView(UpdateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

# @desc --> Delete API View for the DELETE method , @methods --> DELETE
class PostDeleteView(DestroyAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Posts.objects.all()
    serializer_class = PostSerializer



