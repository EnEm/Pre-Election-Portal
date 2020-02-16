from django.urls import path, re_path

from .views import chart,hostelCreateview,hostelDeleteview,hostelUpdateview
app_name='stats'

urlpatterns = [
    path('',chart,name='chart'),
    path('create/',hostelCreateview.as_view(),name='createhostel'),
    path('<int:pk>/delete',hostelDeleteview.as_view(),name='deletehostel'),
    path('<int:pk>/update',hostelUpdateview.as_view(),name='updatehostel'),
    
]