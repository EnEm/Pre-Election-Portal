from django.urls import path, include
from .views import index, user_login, user_logout

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
