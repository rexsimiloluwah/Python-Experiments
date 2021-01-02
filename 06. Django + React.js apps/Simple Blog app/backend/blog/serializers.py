from rest_framework import serializers 
from .models import BlogPost
import os
from users.serializers import UserPublicSerializer


class BlogPostSerializer(serializers.ModelSerializer):

    user = UserPublicSerializer(read_only = True)

    class Meta:
        model = BlogPost

        fields = [
            "user",
            "title",
            "description",
            "id",
            "post_image",
            "content",
            "timestamp",
            "updated",
            "slug",
            "category"
        ]
        

    
        
