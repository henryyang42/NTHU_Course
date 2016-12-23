from django.conf.urls import include, url
from django.contrib import admin
from utils.error_handler import error404

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('search.urls')),
    url(r'^', include('index.urls')),
    url(r'^', include('table.urls')),
]

handler404 = error404
