from rest_framework.generics import ListAPIView
from .serializers import PostSerializer, LookupSerializer
from ..models import *

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LookupListAPIView(ListAPIView):
    queryset = LookupUserInfo.objects.all()
    serializer_class = LookupSerializer

class PostFilter(ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        username=self.kwargs['username']
        return Post.objects.filter(author__username=username)