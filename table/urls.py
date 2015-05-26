from django.conf.urls import patterns, url
import search

urlpatterns = patterns(
    '',
    url(r'^table.html$', search.views.table),
)
