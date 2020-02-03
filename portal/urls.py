from django.urls import path, re_path
from django.views.generic import View

from .views import (
    index,
    user_login,
    user_logout,
    answer_view,
    UpvoteAPIToggle,
    DownvoteAPIToggle,
    load_candidates,
    # SortQuestionsAPI,
)

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    re_path('^(?P<pk>[0-9]+)/$', View.as_view(), name='question'),
    re_path('^api/(?P<pk>[0-9]+)/upvote/$', UpvoteAPIToggle.as_view(), name='api-upvote'),
    re_path('^api/(?P<pk>[0-9]+)/downvote/$', DownvoteAPIToggle.as_view(), name='api-downvote'),
    re_path('^(?P<pk>[0-9]+)/answer/$', answer_view, name='answer'),
    re_path('^ajax/load-candidates/$', load_candidates, name='ajax-load-candidates'),
    # re_path('^api/(?P<ordering>[\w]+)/$', SortQuestionsAPI.as_view(), name='api-sort'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
