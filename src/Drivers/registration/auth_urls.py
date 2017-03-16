
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

from registration.forms import EmailAuthenticationForm


urlpatterns = [
    
    url(r'^login/$',
        auth_views.login, {'authentication_form': EmailAuthenticationForm},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^$', auth_views.password_reset,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_done')},
        name='auth_password_reset'),
     url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
]
