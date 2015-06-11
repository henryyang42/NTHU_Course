from __future__ import absolute_import

import re
import bs4
import requests
import traceback
import progressbar
import threadpool
from threading import Thread
from crawler.course import (
    curriculum_to_trs, course_from_tr, get_syllabus, course_from_syllabus
)
from data_center.models import Course, Department
from data_center.const import week_dict, course_dict

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629002.php'
dept_url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.3/JH623002.php'  # noqa
YS = '104|10'
cond = 'a'
T_YEAR = 104
C_TERM = 10


def dept_2_html(dept, ACIXSTORE, auth_num):
    try:
        r = requests.post(dept_url,
                          data={
                              'SEL_FUNC': 'DEP',
                              'ACIXSTORE': ACIXSTORE,
                              'T_YEAR': T_YEAR,
                              'C_TERM': C_TERM,
                              'DEPT': dept,
                              'auth_num': auth_num})
        r.encoding = 'cp950'
        return r.text
    except:
        print traceback.format_exc()
        print dept
        return 'QAQ, what can I do?'


def cou_code_2_html(cou_code, ACIXSTORE, auth_num):
    try:
        r = requests.post(url,
                          data={
                              'ACIXSTORE': ACIXSTORE,
                              'YS': YS,
                              'cond': cond,
                              'cou_code': cou_code,
                              'auth_num': auth_num})
        r.encoding = 'cp950'
        return r.text
    except:
        print traceback.format_exc()
        print cou_code
        return 'QAQ, what can I do?'


def syllabus_2_html(ACIXSTORE, course):
    try:
        response = get_syllabus(course, ACIXSTORE)
        course_dict = course_from_syllabus(response.text)

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


def trim_syllabus(ACIXSTORE, soup):
    href_garbage = '?ACIXSTORE=%s' % ACIXSTORE
    host = 'https://www.ccxp.nthu.edu.tw'
    # Remove width
    for tag in soup.find_all():
        if 'width' in tag:
            del tag['width']
    # Replace link
    for a in soup.find_all('a'):
        href = a.get('href', '').replace(href_garbage, '').replace(' ', '%20')
        # Make relative path to absolute path
        if 'http' not in href:
            href = host + href
        a['href'] = href
        a['target'] = '_blank'
    syllabus = ''.join(map(unicode, soup.body.contents))
    syllabus = syllabus.replace('</br></br></br></br></br>', '')
    syllabus = syllabus.replace('<br><br><br><br><br>', '')
    return syllabus


def trim_td(td):
    return td.get_text().strip()


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


def crawl_course_info(ACIXSTORE, auth_num, cou_code):
    html = cou_code_2_html(cou_code, ACIXSTORE, auth_num)

    cou_code_stripped = cou_code.strip()
    for tr in curriculum_to_trs(html):
        collect_class_info(tr, cou_code_stripped)


def crawl_course(ACIXSTORE, auth_num, cou_codes):
    threads = []

    for cou_code in cou_codes:
        t = Thread(
            target=crawl_course_info,
            args=(ACIXSTORE, auth_num, cou_code)
        )
        threads.append(t)
        t.start()

    progress = progressbar.ProgressBar()
    for t in progress(threads):
        t.join()

    print 'Crawling syllabus...'
    pool = threadpool.ThreadPool(50)
    reqs = threadpool.makeRequests(
        syllabus_2_html,
        [([ACIXSTORE, course], {}) for course in Course.objects.all()]
    )
    [pool.putRequest(req) for req in reqs]
    pool.wait()

    print 'Total course information: %d' % Course.objects.count()


def crawl_dept_info(ACIXSTORE, auth_num, dept_code):
    html = dept_2_html(dept_code, ACIXSTORE, auth_num)
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
    threads = []

    for dept_code in dept_codes:
        t = Thread(
            target=crawl_dept_info,
            args=(ACIXSTORE, auth_num, dept_code)
        )
        threads.append(t)
        t.start()

    progress = progressbar.ProgressBar()
    for t in progress(threads):
        t.join()

    print 'Total department information: %d' % Department.objects.count()


def get_token(s):
    try:
        return week_dict[s[0]] + course_dict[s[1]] + s[2:]
    except:
        return ''
