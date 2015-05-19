from django.conf.urls import patterns, include, url
from django.contrib import admin
import autocomplete_light

# OP autodiscover
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NTHU_Course.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('search.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^', include('index.urls')),
    url(r'^', include('table.urls')),
)
