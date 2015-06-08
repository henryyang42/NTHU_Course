from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.search),
    url(r'^syllabus/(?P<id>\d+)/$',
        views.syllabus, name='syllabus'),
    url(r'^course/(?P<id>\d+)/$',
        views.course_manipulation, name='course_manipulation'),
    url(r'^status/$', views.courses_status, name='courses_status'),
)
