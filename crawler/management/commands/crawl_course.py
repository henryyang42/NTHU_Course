from django.core.management.base import BaseCommand

from crawler.crawler import crawl_course_info, crawl_dept_info
try:
    from crawler.decaptcha import Entrance, DecaptchaFailure
except ImportError:
    Entrance = None
from data_center.const import cou_codes
from data_center.models import Course, Department


def get_auth_pair(url):
    if Entrance is not None:
        try:
            return Entrance(url).get_ticket()
        except DecaptchaFailure:
            print 'Automated decaptcha failed.'
    else:
        print 'crawler.decaptcha not available (requires tesseract, lxml).'
    print 'Please provide valid ACIXSTORE and auth_num from'
    print url
    ACIXSTORE = raw_input('ACIXSTORE: ')
    auth_num = raw_input('auth_num: ')
    return ACIXSTORE, auth_num


class Command(BaseCommand):
    args = ''
    help = 'Help crawl the course data from NTHU.'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            ACIXSTORE, auth_num = get_auth_pair(
                'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE'
                '/JH/6/6.2/6.2.9/JH629001.php'
            )
            crawl_course_info(ACIXSTORE, auth_num, cou_codes)

            ACIXSTORE, auth_num = get_auth_pair(
                'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE'
                '/JH/6/6.2/6.2.3/JH623001.php'
            )
            crawl_dept_info(ACIXSTORE, auth_num, cou_codes)

        if len(args) == 1:
            if args[0] == 'clear':
                Course.objects.all().delete()
                Department.objects.all().delete()
