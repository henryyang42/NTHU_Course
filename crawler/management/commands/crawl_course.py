from django.core.management.base import BaseCommand

from crawler.crawler import crawl_course_info, crawl_dept_info
from data_center.const import cou_codes
from data_center.models import Course, Department


class Command(BaseCommand):
    args = ''
    help = 'Help crawl the course data from NTHU.'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            print 'Please provide valid ACIXSTORE and auth_num from'
            print 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE' \
                '/JH/6/6.2/6.2.9/JH629001.php'
            ACIXSTORE = raw_input('ACIXSTORE: ')
            auth_num = raw_input('auth_num: ')
            crawl_course_info(ACIXSTORE, auth_num, cou_codes)

            print 'Please provide valid ACIXSTORE and auth_num from'
            print 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE' \
                '/JH/6/6.2/6.2.3/JH623001.php'
            ACIXSTORE = raw_input('ACIXSTORE: ')
            auth_num = raw_input('auth_num: ')
            crawl_dept_info(ACIXSTORE, auth_num, cou_codes)

        if len(args) == 1:
            if args[0] == 'clear':
                Course.objects.all().delete()
                Department.objects.all().delete()
