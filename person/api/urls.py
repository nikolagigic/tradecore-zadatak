from django.conf.urls import url
from .views import PostListAPIView, LookupListAPIView, PostFilter

urlpatterns=[
    url(r'^posts/$', PostListAPIView.as_view(), name='post'),
    url(r'^posts/(?P<username>[\w.@+-]+)/$', PostFilter.as_view(), name='posts-filter'),
    url(r'^lookups/$', LookupListAPIView.as_view(), name='lookup'),
]