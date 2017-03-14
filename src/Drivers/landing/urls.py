from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import StartPageView, Login, Main

urlpatterns = [
    url(r'^$', StartPageView.as_view(), name='start_page'),
    url(r'^login/$', Login.as_view(), 
            name='auth_login'),
    url(r'^main/$',Main.as_view(), name = 'profile'),
    
]