from rest_framework import serializers 
from django.contrib.auth import get_user_model
from api.models import Posts
from api.serializers import PostUserSerializer
from rest_framework.reverse import reverse as drf_reverse

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only = True)
    post_list = serializers.SerializerMethodField(read_only = True)

    
    class Meta:
        model = User
        fields = [
            "id",
            "username", 
            "uri",
            "post_list"
        ]
    
    # Method Field
    def get_uri(self, obj):
        # SYNTAX => drf_reverse("<namespace>:<view_name>", kwargs = {"username" : "username"})
        return f"api/users/{obj.username}/"

    def get_post_list(self, obj):
        qs = Posts.objects.filter(user = obj).order_by("-timestamp")
        return PostUserSerializer(qs, many=True).data
