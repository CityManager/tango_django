from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from tango_django.registration_view import MyRegistrationView

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'tango_django.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^account/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^account/', include('registration.backends.simple.urls')),
]

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)', 'serve',
         {'document_root': settings.MEDIA_ROOT})
    )
