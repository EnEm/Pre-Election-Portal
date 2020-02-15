from django.urls import path, re_path

from . import views
app_name='stats'

urlpatterns = [
    path('',views.chart,name='chart'),
    path('update/',views.update,name='update'),
]