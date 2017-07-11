from rest_framework import serializers
from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
        )
        read_only_fields = (
            'author',
        )