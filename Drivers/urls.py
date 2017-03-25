
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('registration.backends.default.urls')),
    url(r'^', include('Drivers.landing.urls', namespace='landing')),
    url(r'^$', auth_views.password_reset,
        {'post_reset_redirect': reverse_lazy('auth_login')},
        name='prelogin'),
]
