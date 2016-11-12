from __future__ import absolute_import

import re
import bs4
import traceback
import progressbar
from itertools import zip_longest
from requests_futures.sessions import FuturesSession
from django.db import transaction
from crawler.course import (
    curriculum_to_trs, course_from_tr, syllabus_url, course_from_syllabus,
    form_action_url, dept_url, encoding
)
from data_center.models import Course, Department
from data_center.const import week_dict, course_dict

MAX_WORKERS = 8  # max_workers for FuturesSession


def ys_2_year_term(ys):
    return tuple(ys.split('|'))


def dept_2_future(session, dept, acixstore, auth_num, ys):
    year, term = ys_2_year_term(ys)

    return session.post(
        dept_url,
        data={
            'SEL_FUNC': 'DEP',
            'ACIXSTORE': acixstore,
            'T_YEAR': year,
            'C_TERM': term,
            'DEPT': dept,
            'auth_num': auth_num})


def cou_code_2_future(session, cou_code, acixstore, auth_num, ys):
    return session.post(
        form_action_url,
        data={
            'ACIXSTORE': acixstore,
            'YS': ys,  # year|term
            'cond': 'a',
            'cou_code': cou_code,
            'auth_num': auth_num})


def save_syllabus(html, course, ys):
    try:
        course_dict = course_from_syllabus(html)

        course.chi_title = course_dict['name_zh']
        course.eng_title = course_dict['name_en']
        course.credit = course_dict['credit']
        course.time = course_dict['time']
        course.time_token = get_token(course_dict['time'])
        course.teacher = course_dict['teacher']
        course.room = course_dict['room']
        course.syllabus = course_dict['syllabus']
        course.has_attachment = course_dict['has_attachment']
        course.ys = ys
        course.save()
    except:
        print(traceback.format_exc())
        print(course)
        return 'QAQ, what can I do?'


def collect_class_info(tr, cou_code):
    course_dict = course_from_tr(tr)

    course, create = Course.objects.get_or_create(no=course_dict['no'])

    if cou_code not in course.code:
        course.code = '%s %s' % (course.code, cou_code)

    # these data are available in the syllabus, use those!
    # course.credit = course_dict['credit']
    # course.time = course_dict['time']
    # course.time_token = get_token(course_dict['time'])
    course.limit = course_dict['size_limit'] or 0
    course.note = course_dict['note']
    course.objective = course_dict['object']
    course.prerequisite = course_dict['has_prerequisite']
    course.ge = course_dict['ge_hint'] or ''
    course.save()

    return create


def handle_curriculum_html(html, cou_code):
    cou_code_stripped = cou_code.strip()
    for tr in curriculum_to_trs(html):
        collect_class_info(tr, cou_code_stripped)


def crawl_course(acixstore, auth_num, cou_codes, ys):
    with FuturesSession(max_workers=MAX_WORKERS) as session:
        curriculum_futures = [
            cou_code_2_future(session, cou_code, acixstore, auth_num, ys)
            for cou_code in cou_codes
        ]

        progress = progressbar.ProgressBar(maxval=len(cou_codes))
        with transaction.atomic():
            for future, cou_code in progress(
                zip(curriculum_futures, cou_codes)
            ):
                response = future.result()
                response.encoding = 'cp950'
                handle_curriculum_html(response.text, cou_code)

    print('Crawling syllabus...')
    course_list = list(Course.objects.all())

    with FuturesSession(max_workers=MAX_WORKERS) as session:
        course_futures = [
            session.get(
                syllabus_url,
                params={
                    'c_key': course.no,
                    'ACIXSTORE': acixstore,
                }
            )
            for course in course_list
        ]

        progress = progressbar.ProgressBar(maxval=len(course_list))
        for future, course in progress(zip_longest(
            course_futures, course_list
        )):
            response = future.result()
            response.encoding = 'cp950'
            save_syllabus(response.text, course, ys)

        print('Total course information: %d' % Course.objects.filter(ys=ys).count())  # noqa


def handle_dept_html(html, ys):
    soup = bs4.BeautifulSoup(html, "lxml")
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
            ys=ys, dept_name=dept_name)[0]

        for tr in trs:
            tds = tr.find_all('td')
            cou_no = tds[0].get_text()
            try:
                course = Course.objects.get(ys=ys, no__contains=cou_no)
                department.required_course.add(course)
                department.save()
            except:
                print(cou_no, 'gg')


def crawl_dept(acixstore, auth_num, dept_codes, ys):
    with FuturesSession(max_workers=MAX_WORKERS) as session:
        future_depts = [
            dept_2_future(session, dept_code, acixstore, auth_num, ys)
            for dept_code in dept_codes
        ]

        progress = progressbar.ProgressBar()
        with transaction.atomic():
            for future in progress(future_depts):
                response = future.result()
                response.encoding = encoding
                handle_dept_html(response.text, ys)

    print('Total department information: %d' % Department.objects.filter(ys=ys).count())  # noqa


def get_token(s):
    try:
        return week_dict[s[0]] + course_dict[s[1]] + s[2:]
    except:
        return ''
