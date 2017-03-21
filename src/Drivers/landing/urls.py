from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import   Main , Action, Choose, Final, Result


app_name = 'landing'
urlpatterns = [
    url(r'^main/choose$', Choose.as_view(), name= 'choose'),
    url(r'^main/$',Main.as_view(), name = 'profile'),
    url(r'^main/action/$' ,Action.as_view(), name='action'),
    url(r'^final/$', Final.as_view(), name='final'),
    url(r'^result/$', Result.as_view(), name='result'),
]