from django.conf.urls import patterns, url
import search
import table.views

urlpatterns = patterns(
    '',
    url(r'^table.html$', search.views.table),
    url(r'^prerequisites.html$', table.views.prerequisite),
)
