from django.urls import path, re_path

from .views import chart, HostelCreateview, hostelDeleteview, HostelUpdateview

app_name = 'stats'

urlpatterns = [
    path('', chart, name='chart'),
    path('create/', HostelCreateview.as_view(), name='createhostel'),
    path('<int:pk>/delete', hostelDeleteview.as_view(), name='deletehostel'),
    path('<int:pk>/update', HostelUpdateview.as_view(), name='updatehostel'),

]
