import re
import bs4
import requests
import traceback
import progressbar
import threadpool
from threading import Thread
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
        return r.content.decode('big5', 'ignore').encode('utf8', 'ignore')
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
        return r.content.decode('big5', 'ignore').encode('utf8', 'ignore')
    except:
        print traceback.format_exc()
        print cou_code
        return 'QAQ, what can I do?'


def syllabus_2_html(ACIXSTORE, course):
    url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/common/Syllabus/1.php?ACIXSTORE=%s&c_key=%s' % (ACIXSTORE, course.no.replace(' ', '%20'))  # noqa
    try:
        while True:
            r = requests.get(url)
            html = r.content.decode('big5', 'ignore').encode('utf8', 'ignore')
            soup = bs4.BeautifulSoup(html, 'html.parser')
            tables = soup.find_all('table')
            if tables:
                trs = tables[0].find_all('tr')
                break
            else:
                continue
        for i in range(2, 5):
            trs[i].find_all('td')[1]['colspan'] = 5
        course.chi_title = trs[2].find_all('td')[1].get_text()
        course.eng_title = trs[3].find_all('td')[1].get_text()
        course.teacher = trs[4].find_all('td')[1].get_text()
        course.room = trs[5].find_all('td')[3].get_text()
        course.syllabus = trim_syllabus(ACIXSTORE, soup)
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
    tds = tr.find_all('td')

    no = trim_td(tds[0])
    time = trim_td(tds[3])
    note = trim_td(tds[7])
    objective = trim_td(tds[9])
    prerequisite = trim_td(tds[10])
    credit = trim_td(tds[2])
    credit = int(credit) if credit.isdigit() else 0
    limit = trim_td(tds[6])
    limit = int(limit) if limit.isdigit() else 0
    ge = ''
    title = tds[1].contents
    if len(title) > 1:
        title = title[1].contents
        if len(title) > 1:
            ge = title[1].get_text().strip()

    course, create = Course.objects.get_or_create(no=no)

    if cou_code not in course.code:
        course.code = '%s %s' % (course.code, cou_code)

    course.credit = credit
    course.time = time
    course.time_token = get_token(time)
    course.limit = limit
    course.note = note
    course.objective = objective
    course.prerequisite = prerequisite
    course.ge = ge
    course.save()

    return create


def crawl_course_info(ACIXSTORE, auth_num, cou_code):
    html = cou_code_2_html(cou_code, ACIXSTORE, auth_num)
    soup = bs4.BeautifulSoup(html, 'html.parser')

    trs = soup.find_all('tr', class_='class3')
    trs = [tr for tr in trs if len(tr.find_all('td')) > 1]
    for tr in trs:
        collect_class_info(
            tr, cou_code.strip()
        )


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
    pool = threadpool.ThreadPool(250)
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
