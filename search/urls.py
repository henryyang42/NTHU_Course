from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.search),
    url(r'^syllabus/(?P<id>\d+)/$', views.syllabus, name='syllabus'),
    url(r'^hit/(?P<id>\d+)/$', views.hit, name='hit'),
)
