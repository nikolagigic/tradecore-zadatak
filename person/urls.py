from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$', home, name='home'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'log-auth/$', log_auth, name='log-auth'),
    url(r'reg-check/$', reg_check, name='reg-check'),
    url(r'logout/$', logout, name='logout'),
    url(r'like/$', like, name='like'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', profile, name='profile'),
    url(r'new-post/$', new_post, name='new-post'),
]