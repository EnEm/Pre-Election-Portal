from django.urls import path, re_path
from django.views.generic import View

from .views import index, user_login, user_logout, UpvoteToggleView, DownvoteToggleView

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    re_path('^(?P<pk>[0-9]+)/$', View.as_view(), name='question'),
    re_path('^(?P<pk>[0-9]+)/upvote/$', UpvoteToggleView.as_view(), name='upvote'),
    re_path('^(?P<pk>[0-9]+)/downvote/$', DownvoteToggleView.as_view(), name='downvote'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
