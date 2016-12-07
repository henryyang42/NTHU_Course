from django.conf.urls import url
from .views import search, syllabus, hit, autocomplete

urlpatterns = [
    url(r'^$', search),
    url(r'^syllabus/(?P<no>.+)/$',
        syllabus, name='syllabus'),
    url(r'^hit/(?P<no>.+)/$', hit, name='hit'),
    url(r'^autocomplete/$', autocomplete, name='autocomplete'),
]
