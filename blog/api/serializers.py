from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.api.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """API serializer for User model"""

    class Meta:
        model = get_user_model()
        fields = ["url", "username", "email", "groups", "password"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """API serializer for Post model"""

    class Meta:
        model = Post
        fields = ["id", "title", "url", "body", "user", "created"]
