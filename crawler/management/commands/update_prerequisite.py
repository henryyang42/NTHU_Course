from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.template import Context

from crawler.prerequisite import get_prerequisites
from data_center.models import FlatPrerequisite


class Command(BaseCommand):
    args = ''
    help = 'update prerequisite html in database'

    def handle(self, *args, **kwargs):
        template = get_template('prerequisite_table.html')

        # care needs to be taken if we are going to upgrade to django>=1.8
        # docs.djangoproject.com/en/1.8/ref/templates/upgrading/#template
        html = template.render(
            Context({'pdata': sorted(get_prerequisites().items())}))

        FlatPrerequisite.update_html(html)
