from django.conf.urls import url
from authentication import views

app_name = 'authentication'
urlpatterns = [
    # The home view ('/authentication/')
    url(r'^$', views.home, name='home'),
    # Explicit home ('/authentication/home/')
    url(r'^home/$', views.home, name='home'),
    # Redirect to get token ('/authentication/gettoken/')
    url(r'^gettoken/$', views.gettoken, name='gettoken'),
]
