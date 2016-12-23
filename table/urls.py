from django.conf.urls import url
import search
import table.views

urlpatterns = [
    url(r'^table.html$', search.views.table),
    url(r'^prerequisites.html$', table.views.prerequisite),
]
