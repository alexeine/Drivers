
from django.conf.urls import url,include
from django.contrib import admin
#import registration.backends.default.urls
#import django.contrib.sites
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
