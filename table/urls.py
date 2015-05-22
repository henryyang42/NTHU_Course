from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import search

urlpatterns = patterns(
    '',
    url(r'^table.html$', search.views.table),
)

