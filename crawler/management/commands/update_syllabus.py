from django.core.management.base import BaseCommand

from crawler.crawler import update_syllabus
from data_center.const import cou_codes
from data_center.models import Course, Department


class Command(BaseCommand):
    args = ''
    help = 'Help crawl the course syllabus from NTHU.'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            update_syllabus()



