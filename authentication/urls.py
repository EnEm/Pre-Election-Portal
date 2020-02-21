from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
    path('signout', views.sign_out, name='signout'),
    path('save-session', views.save_session, name='save-session'),
]