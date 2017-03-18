from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import StartPageView,  Main , Action

urlpatterns = [
    url(r'^$', StartPageView.as_view(), name='start_page'),
    url(r'^main/$',Main.as_view(), name = 'profile'),
    url(r'^main/action/$' ,Action.as_view(), name='action'),
]