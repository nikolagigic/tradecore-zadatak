from rest_framework.serializers import ModelSerializer
from person.models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'title',
            'content',
        ]