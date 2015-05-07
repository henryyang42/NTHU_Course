from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns(
    '',
    url(r'^table.html$', TemplateView.as_view(template_name='table.html')),
)

