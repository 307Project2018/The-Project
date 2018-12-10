from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.urls import path, include # new

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^TeraChess/', include('TeraChess.urls')),
    url(r'accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('', RedirectView.as_view(url='/TeraChess/index', permanent=True)),
]
STATIC_URL = '/static/'
