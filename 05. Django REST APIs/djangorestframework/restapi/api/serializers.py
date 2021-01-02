from rest_framework import serializers 

from .models import Posts

from accounts.api.serializers import UserPublicSerializer

class PostUserSerializer(serializers.ModelSerializer):  # Serializer to be used in the Users file
    uri = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Posts
        fields = [
            "id",
            "content",
            "post_image",
            "uri"
        ]

    def get_uri(self, obj):
        return f"api/posts/{obj.id}"


class PostSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only = True)
    # Serializer Related Field
    user_name = serializers.SlugRelatedField(source = 'user',read_only=True, slug_field="username" )
    class Meta:
        model = Posts
        fields = [
            "id",
            "user",
            "content",
            "post_image",
            "user_name"
        ]

        # The read_only_field attribute ensures that the field cannot be altered or written to (Typically used for default fields or user fields)
        read_only_fields = ["user"]

    # Validation 
    def validate_content(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError("Content cannot be more than 1000 characters !")
        return value

    def validate(self, data):
        content = data.get("content", None)
        image = data.get("image", None)

        if content == "":
            content == None

        if content == None and image == None:
            raise serializers.ValidationError("Content or Image are Required !")

        return data
