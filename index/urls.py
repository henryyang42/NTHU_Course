from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^index.html$', TemplateView.as_view(template_name='index.html')),
    url(r'^donate.html$', TemplateView.as_view(template_name='donate.html')),
    url(r'^todo-list.html$', TemplateView.as_view(template_name='todo-list.html')),
    url(r'^hiring.html$', TemplateView.as_view(template_name='hiring.html')),
    url(r'^privatepolicy.html$', TemplateView.as_view(template_name='privatepolicy.html')),
    url(r'^404.html$', TemplateView.as_view(template_name='404.html')),
)
