import re
import bs4
import requests
import traceback
import progressbar
from data_center.models import Course, Department
from data_center.const import week_dict, course_dict

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629002.php'
dept_url = \
    'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.3/JH623002.php'
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
        return r.text.encode('latin1', 'ignore') \
            .decode('big5', 'ignore').encode('utf8', 'ignore')
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
        return r.text.encode('latin1', 'ignore') \
            .decode('big5', 'ignore').encode('utf8', 'ignore')
    except:
        print traceback.format_exc()
        print cou_code
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
        a['href'] = a['href'].replace(href_garbage, '').replace(' ', '%20')
        # Make relative path to absolute path
        if 'www' not in a['href'] or 'http' not in a['href']:
            a['href'] = host + a['href']

    syllabus = ''.join(map(unicode, soup.body.contents))
    syllabus = syllabus.replace('</br></br></br></br></br>', '')
    syllabus = syllabus.replace('<br><br><br><br><br>', '')
    return syllabus


def syllabus_2_html(ACIXSTORE, course):
    url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/' \
        'common/Syllabus/1.php?ACIXSTORE=%s&c_key=%s' % \
        (ACIXSTORE, course.no.replace(' ', '%20'))
    try:
        while True:
            r = requests.get(url)
            html = r.text.encode('latin1', 'ignore'). \
                decode('big5', 'ignore').encode('utf8', 'ignore')
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
        course.save()
        course.syllabus = trim_syllabus(ACIXSTORE, soup)
        course.save()
    except:
        print traceback.format_exc()
        print course
        return 'QAQ, what can I do?'


def trim_td(td):
    return td.get_text().rstrip().lstrip()


def tr_2_class_info(tr):
    tds = tr.find_all('td')
    class_info = {
        'no': trim_td(tds[0]),
        'title': tds[1],
        'credit': trim_td(tds[2]),
        'time': trim_td(tds[3]),
        'limit': trim_td(tds[6]),
        'note': trim_td(tds[7]),
        'objective': trim_td(tds[9]),
        'prerequisite': trim_td(tds[10])
    }
    return class_info


def get_ge(title):
    title = title.contents
    if len(title) > 1:
        title = title[1].contents
        if len(title) > 1:
            title = title[1].get_text()
            title = title.rstrip().lstrip()
            return title
    return ''


def crawl_course_info(ACIXSTORE, auth_num, cou_codes):
    progress = progressbar.ProgressBar()
    total_collected = 0
    for cou_code in progress(cou_codes):
        html = cou_code_2_html(cou_code, ACIXSTORE, auth_num)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr', class_='class3')
        trs = [tr for tr in trs if len(tr.find_all('td')) > 1]
        for tr in trs:
            class_info = tr_2_class_info(tr)
            if Course.objects.filter(no=class_info['no']):
                continue
            if not class_info['credit'].isdigit():
                class_info['credit'] = '0'
            if not class_info['limit'].isdigit():
                class_info['limit'] = '0'
            course = Course.objects.update_or_create(
                no=class_info['no'],
                credit=int(class_info['credit']),
                time=class_info['time'],
                time_token=get_token(class_info['time']),
                limit=int(class_info['limit']),
                note=class_info['note'],
                objective=class_info['objective'],
                prerequisite=class_info['prerequisite'] != '',
                code=cou_code.strip(),
                ge=get_ge(class_info['title']),
            )[0]

            syllabus_2_html(ACIXSTORE, course)
            total_collected += 1

    print '%d course information collected.' % total_collected


def crawl_dept_info(ACIXSTORE, auth_num, dept_codes):
    progress = progressbar.ProgressBar()
    total_collected = 0
    for dept_code in progress(dept_codes):
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
            total_collected += 1

    print '%d department information collected.' % total_collected


def update_syllabus():
    r = requests.get(
        'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629001.php'
    )
    ACIXSTORE = bs4.BeautifulSoup(r.text, 'html.parser').find('input')['value']
    progress = progressbar.ProgressBar()
    for course in progress(Course.objects.all()):
        syllabus_2_html(ACIXSTORE, course)


def get_token(s):
    try:
        return week_dict[s[0]] + course_dict[s[1]] + s[2:]
    except:
        return ''
