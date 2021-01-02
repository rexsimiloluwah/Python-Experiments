from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView

# Create your views here.

class BlogPostListView(ListAPIView, CreateAPIView):
    queryset = BlogPost.objects.order_by("-timestamp")
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

class BlogPostDetailView(UpdateAPIView, RetrieveAPIView):
    queryset = BlogPost.objects.order_by("-timestamp")
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    lookup_field = "slug"

class BlogPostFeaturedView(ListAPIView):
    queryset = BlogPost.objects.all().filter(featured = True)
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

class BlogPostCategoryView(APIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = BlogPost.objects.all()

    def post(self, request):
        data = self.request.data
        category = data.get("category", None)

        if category == "all":
            queryset = BlogPost.objects.all()
        else:
            queryset = BlogPost.objects.filter(category__iexact = category)
            
        serialized_data = BlogPostSerializer(queryset, many = True, context = {"request" : request}).data
        # print(serialized_data)
        return Response(serialized_data, status = status.HTTP_200_OK)



