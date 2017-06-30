from rest_framework.serializers import ModelSerializer, SerializerMethodField
from person.models import *

class PostSerializer(ModelSerializer):

    author=SerializerMethodField()

    def get_author(self, obj):
        full_name=obj.author.name+' '+obj.author.surname
        return full_name

    class Meta:
        model=Post
        fields=[
            'author',
            'title',
            'content',
            'likes',
        ]


class LookupSerializer(ModelSerializer):
    class Meta:
        model=LookupUserInfo
        fields=[
            'givenName',
            'familyName',
            'email',
            'gender',
            'location',
            'timeZone',
            'bio',
            'site',
        ]