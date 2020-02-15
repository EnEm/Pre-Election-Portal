from django.urls import path, re_path

from .views import graph
app_name='stats'

urlpatterns = [
    path('',graph,name='graph')
]