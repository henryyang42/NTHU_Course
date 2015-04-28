import re
import urllib2
import bs4
import json
import requests
import sys
import traceback
import progressbar

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629002.php'
ACIXSTORE = 'as7c6glo9o4iqeudcif4rbo002'
YS = '103|20'
cond = 'a'
auth_num = '125'

cou_codes = ['ANTH', 'ANTU', 'ASTR', 'BME ', 'BMES', 'CF ', 'CFGE', 'CHE ', 'CHEM', 'CL ', 'CLC ', 'CLU ', 'COM ', 'CS ', 'DL ', 'DMS ', 'E ', 'ECON', 'EE ', 'EECS', 'EMBA', 'ENE ', 'ESS ', 'FL ', 'FLU ', 'GE ', 'GEC ', 'GEU ', 'GPTS', 'HIS ', 'HSS ', 'HSSU', 'IACS', 'IACU', 'IEEM', 'IEM ', 'ILS ', 'IMBA', 'IPE ', 'IPNS', 'IPT ', 'ISA ', 'ISS ', 'LANG', 'LING', 'LS ', 'LSBS', 'LSBT', 'LSIP', 'LSMC', 'LSMM', 'LSSN', 'LST ', 'MATH', 'MATU', 'MBA ', 'MI ', 'MS ', 'NEMS', 'NES ', 'NS ', 'NUCL', 'PE ', 'PE1 ', 'PE3 ', 'PHIL', 'PHYS', 'PHYU', 'PME ', 'QF ', 'RB ', 'RDDM', 'RDIC', 'RDPE', 'SCI ', 'SLS ', 'SNHC', 'SOC ', 'STAT', 'STAU', 'TE ', 'TEG ', 'TEX ', 'TIGP', 'TL ', 'TM ', 'UPMT', 'W ', 'WH ', 'WW ', 'WZ ', 'X ', 'XA ', 'XZ ', 'YZ ', 'ZY ', 'ZZ ']


def cou_code_2_html(cou_code):
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


def trim_td(td):
    return td.get_text().rstrip().lstrip().encode('utf8', 'ignore')


def tr_2_class_info(tr):
    tds = tr.find_all('td')
    class_info = {
        'no': trim_td(tds[0]),
        'title': trim_td(tds[1]),
        'credit': trim_td(tds[2]),
        'time': trim_td(tds[3]),
        'room': trim_td(tds[4]),
        'teacher': trim_td(tds[5]),
        'limit': trim_td(tds[6]),
        'note': trim_td(tds[7]),
        'object': trim_td(tds[9]),
        'prerequisite': trim_td(tds[10])
    }
    return class_info

progress = progressbar.ProgressBar()
class_infos = []

for cou_code in progress(cou_codes):
    html = cou_code_2_html(cou_code)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    trs = [tr for tr in trs if 'class3' in tr['class'] and len(tr.find_all('td')) > 1]
    for tr in trs:
        try:
            class_info = tr_2_class_info(tr)
            class_infos.append(class_info)
        except :
            print 'QAQ, what can I do?'
            print traceback.format_exc()

f = open('result.txt', 'w')
f.write(json.dumps(class_infos ,ensure_ascii=False, indent=2))
f.close()

