from __future__ import absolute_import

import re
import bs4
import grequests
import traceback
import progressbar
import itertools
from django.db import transaction
from crawler.course import (
    curriculum_to_trs, course_from_tr, syllabus_url, course_from_syllabus
)
from data_center.models import Course, Department
from data_center.const import week_dict, course_dict

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629002.php'
dept_url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.3/JH623002.php'  # noqa
YS = '104|10'
cond = 'a'
T_YEAR = 104
C_TERM = 10


def dept_2_response(dept, ACIXSTORE, auth_num):
    return grequests.post(
        dept_url,
        data={
            'SEL_FUNC': 'DEP',
            'ACIXSTORE': ACIXSTORE,
            'T_YEAR': T_YEAR,
            'C_TERM': C_TERM,
            'DEPT': dept,
            'auth_num': auth_num})


def cou_code_2_response(cou_code, ACIXSTORE, auth_num):
    return grequests.post(
        url,
        data={
            'ACIXSTORE': ACIXSTORE,
            'YS': YS,
            'cond': cond,
            'cou_code': cou_code,
            'auth_num': auth_num})


def save_syllabus(html, course):
    try:
        course_dict = course_from_syllabus(html)

        course.chi_title = course_dict['name_zh']
        course.eng_title = course_dict['name_en']
        course.teacher = course_dict['teacher']
        course.room = course_dict['room']
        course.syllabus = course_dict['syllabus']
        course.save()
    except:
        print traceback.format_exc()
        print course
        return 'QAQ, what can I do?'


def collect_class_info(tr, cou_code):
    course_dict = course_from_tr(tr)

    course, create = Course.objects.get_or_create(no=course_dict['no'])

    if cou_code not in course.code:
        course.code = '%s %s' % (course.code, cou_code)

    course.credit = course_dict['credit']
    course.time = course_dict['time']
    course.time_token = get_token(course_dict['time'])
    course.limit = course_dict['size_limit']
    course.note = course_dict['note']
    course.objective = course_dict['object']
    course.prerequisite = course_dict['prerequisite']
    course.ge = course_dict['ge_hint'] or ''
    course.save()

    return create


def handle_curriculum_html(html, cou_code):
    cou_code_stripped = cou_code.strip()
    for tr in curriculum_to_trs(html):
        collect_class_info(tr, cou_code_stripped)


def crawl_course(ACIXSTORE, auth_num, cou_codes):
    grs = (
        cou_code_2_response(cou_code, ACIXSTORE, auth_num)
        for cou_code in cou_codes
    )
    progress = progressbar.ProgressBar(maxval=len(cou_codes))
    for response, cou_code in progress(
        itertools.izip(grequests.imap(grs), cou_codes)
    ):
        response.encoding = 'cp950'
        handle_curriculum_html(response.text, cou_code)

    print 'Crawling syllabus...'
    course_list = list(Course.objects.all())

    grs = (
        grequests.get(
            syllabus_url,
            params={
                'c_key': course.no,
                'ACIXSTORE': ACIXSTORE,
            }
        )
        for course in course_list
    )

    progress = progressbar.ProgressBar(maxval=len(course_list))
    with transaction.atomic():
        for response, course in progress(
            itertools.izip(grequests.imap(grs), course_list)
        ):
            response.encoding = 'cp950'
            save_syllabus(response.text, course)

    print 'Total course information: %d' % Course.objects.count()


def handle_dept_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='newpage')

    for div in divs:
        # Get something like ``EE  103BA``
        dept_name = div.find_all('font')[0].get_text().strip()
        dept_name = dept_name.replace('B A', 'BA')
        dept_name = dept_name.replace('B B', 'BB')
        try:
            dept_name = re.search('\((.*?)\)', dept_name).group(1)
        except:
            # For all student (Not important for that dept.)
            continue

        trs = div.find_all('tr', bgcolor="#D8DAEB")
        department = Department.objects.get_or_create(
            dept_name=dept_name)[0]
        for tr in trs:
            tds = tr.find_all('td')
            cou_no = tds[0].get_text()
            try:
                course = Course.objects.get(no__contains=cou_no)
                department.required_course.add(course)
            except:
                print cou_no, 'gg'
        department.save()


def crawl_dept(ACIXSTORE, auth_num, dept_codes):
    grs = (
        dept_2_response(dept_code, ACIXSTORE, auth_num)
        for dept_code in dept_codes
    )

    progress = progressbar.ProgressBar(maxval=len(dept_codes))
    with transaction.atomic():
        for response in progress(grequests.imap(grs)):
            response.encoding = 'cp950'
            handle_dept_html(response.text)

    print 'Total department information: %d' % Department.objects.count()


def get_token(s):
    try:
        return week_dict[s[0]] + course_dict[s[1]] + s[2:]
    except:
        return ''
