import re
import urllib2
import bs4
import json
import requests
import sys
import traceback
import progressbar
from data_center.models import *

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629002.php'
YS = '103|20'
cond = 'a'

cou_codes = ['ANTH', 'ANTU', 'ASTR', 'BME ', 'BMES', 'CF ', 'CFGE', 'CHE ', 'CHEM', 'CL ', 'CLC ', 'CLU ', 'COM ', 'CS ', 'DL ', 'DMS ', 'E ', 'ECON', 'EE ', 'EECS', 'EMBA', 'ENE ', 'ESS ', 'FL ', 'FLU ', 'GE ', 'GEC ', 'GEU ', 'GPTS', 'HIS ', 'HSS ', 'HSSU', 'IACS', 'IACU', 'IEEM', 'IEM ', 'ILS ', 'IMBA', 'IPE ', 'IPNS', 'IPT ', 'ISA ', 'ISS ', 'LANG', 'LING', 'LS ', 'LSBS', 'LSBT', 'LSIP', 'LSMC', 'LSMM', 'LSSN', 'LST ', 'MATH', 'MATU', 'MBA ', 'MI ', 'MS ', 'NEMS', 'NES ', 'NS ', 'NUCL', 'PE ', 'PE1 ', 'PE3 ', 'PHIL', 'PHYS', 'PHYU', 'PME ', 'QF ', 'RB ', 'RDDM', 'RDIC', 'RDPE', 'SCI ', 'SLS ', 'SNHC', 'SOC ', 'STAT', 'STAU', 'TE ', 'TEG ', 'TEX ', 'TIGP', 'TL ', 'TM ', 'UPMT', 'W ', 'WH ', 'WW ', 'WZ ', 'X ', 'XA ', 'XZ ', 'YZ ', 'ZY ', 'ZZ ']


def cou_code_2_html(cou_code, ACIXSTORE, auth_num):
    try:
        r = requests.post(url,
            data={
                'ACIXSTORE': ACIXSTORE,
                'YS': YS,
                'cond': cond,
                'cou_code': cou_code,
                'auth_num': auth_num})
        return r.text.encode('latin1', 'ignore').decode('big5', 'ignore')
    except:
        print traceback.format_exc()
        print cou_code
        return 'QAQ, what can I do?'

def trim_syllabus(ACIXSTORE, soup):
    href_garbage = '?ACIXSTORE=%s' % ACIXSTORE
    host = 'https://www.ccxp.nthu.edu.tw'
    # Replace link
    for a in soup.findAll('a'):
        a['href'] = a['href'].replace(href_garbage, '').replace(' ', '%20')
        # Make relative path to absolute path
        if 'www' not in a['href'] or 'http' not in a['href']:
            a['href'] = host + a['href']

    syllabus = ''.join(map(str, soup.body.contents))
    syllabus = syllabus.replace('</br></br></br></br></br>', '')
    return syllabus

def syllabus_2_html(ACIXSTORE, course):
    url = \
        'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/common/Syllabus/1.php?ACIXSTORE=%s&c_key=%s' % \
        (ACIXSTORE, course.no.replace(' ', '%20'))
    try:
        r = requests.get(url)
        html = r.text.encode('latin1', 'ignore'). \
            decode('big5', 'ignore').encode('utf8', 'ignore')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('table')[0].find_all('tr')
        for i in range(2, 5):
            trs[i].find_all('td')[1]['colspan'] = 5
        course.chi_title = trs[2].find_all('td')[1].get_text()
        course.eng_title = trs[3].find_all('td')[1].get_text()
        course.teacher = trs[4].find_all('td')[1].get_text()
        course.syllabus = trim_syllabus(ACIXSTORE, soup)
        course.save()
    except:
        print traceback.format_exc()
        print course
        return 'QAQ, what can I do?'

def trim_td(td):
    return td.get_text().rstrip().lstrip().encode('utf8', 'ignore')


def tr_2_class_info(tr):
    tds = tr.find_all('td')
    class_info = {
        'no': trim_td(tds[0]),
        'credit': trim_td(tds[2]),
        'time': trim_td(tds[3]),
        'room': trim_td(tds[4]),
        'limit': trim_td(tds[6]),
        'note': trim_td(tds[7]),
        'object': trim_td(tds[9]),
        'prerequisite': trim_td(tds[10])
    }
    return class_info


def initial_db(ACIXSTORE, auth_num):
    progress = progressbar.ProgressBar()
    class_infos = []
    total_collected = 0
    fail = 0
    for cou_code in progress(cou_codes):
        html = cou_code_2_html(cou_code, ACIXSTORE, auth_num)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        trs = [tr for tr in trs if 'class3' in tr['class'] and len(tr.find_all('td')) > 1]
        for tr in trs:
            class_info = tr_2_class_info(tr)
            class_infos.append(class_info)
            if not class_info['credit']:
                class_info['credit'] = '0'
            if not class_info['limit']:
                class_info['limit'] = '0'
            Course.objects.filter(no=class_info['no']).delete()
            course = Course.objects.create(
                no=class_info['no'],
                credit=int(class_info['credit']),
                time=class_info['time'],
                room=class_info['room'],
                limit=int(class_info['limit']),
                note=class_info['note'],
                object=class_info['object'],
                prerequisite=class_info['prerequisite'] != '',
                code=cou_code.strip(),
            )
            syllabus_2_html(ACIXSTORE, course)
            total_collected += 1


    print 'Crawling process is done. %d course information collected.' % total_collected

