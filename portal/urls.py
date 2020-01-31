from django.urls import path, re_path
from django.views.generic import View

from .views import (
    index,
    user_login,
    user_logout,
    UpvoteAPIToggle,
    DownvoteAPIToggle,
)

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    re_path('^(?P<pk>[0-9]+)/$', View.as_view(), name='question'),
    re_path('^api/(?P<pk>[0-9]+)/upvote/$', UpvoteAPIToggle.as_view(), name='api-upvote'),
    re_path('^api/(?P<pk>[0-9]+)/downvote/$', DownvoteAPIToggle.as_view(), name='api-downvote'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
