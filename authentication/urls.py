from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
    path('signout', views.sign_out, name='signout'),
]