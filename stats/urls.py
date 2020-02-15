from django.urls import path, re_path

from .views import chart
app_name='stats'

urlpatterns = [
    path('',chart,name='graph')
]