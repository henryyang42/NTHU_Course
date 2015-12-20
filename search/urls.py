from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.search),
    url(r'^syllabus/(?P<no>.+)/$',
        views.syllabus, name='syllabus'),
    url(r'^hit/(?P<no>.+)/$', views.hit, name='hit'),
)
