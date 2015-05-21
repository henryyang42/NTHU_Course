# -*- coding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from data_center.models import Course, Department
from django.db.models import Q
from django.views.decorators.cache import cache_page

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
# Create your views here.
import re

CLASS_NAME_MAP = {'1': 'BA', '2': 'BB', '3': 'BC', '5': 'M',
                  '6': 'M', '7': 'M', '8': 'D', '9': 'D'}
DEPT_MAP = {'000': 'ST', '001': 'SLS', '002': 'ILS', '010': 'IPNS', '011': 'ESS', '012': 'BMES', '013': 'NES', '020': 'SCI', '021': 'MATH', '022': 'PHYS', '023': 'CHEM', '024': 'STAT', '025': 'ASTR', '030': 'IPE', '031': 'MS', '032': 'CHE', '033': 'PME', '034': 'IEEM', '035': 'NEMS', '036': 'IEM', '037': 'OET', '038': 'BME', '041': 'CL', '042': 'FL', '043': 'HIS', '044': 'LING', '045': 'SOC', '046': 'ANTH', '047': 'PHIL',
            '048': 'HSS', '049': 'TL', '141': 'GPTS', '142': 'IACS', '060': 'EECS', '061': 'EE', '062': 'CS', '063': 'ENE', '064': 'COM', '065': 'ISA', '066': 'IPT', '067': 'RDIC', '068': 'RDDM', '069': 'RDPE', '161': 'UPPP', '162': 'SNHC', '070': 'UPMT', '071': 'QF', '072': 'ECON', '073': 'TM', '074': 'LST', '075': 'EMBA', '076': 'MBA', '077': 'IMBA', '078': 'ISS', '080': 'LSIP', '081': 'LS', '082': 'DMS', '083': 'LSIN'}


def get_class_name(c):
    return CLASS_NAME_MAP.get(c, 'B')


def get_dept(no):
    if len(no) < len('101062124') - 1:
        return ''
    if len(no) == len('101062142') - 1:
        no = '0' + no
    year = no[0:3]
    dept = no[3:6]
    dept = DEPT_MAP.get(dept, '')
    class_name = no[6:7]
    if dept:
        return '%-4s%s%s' % (dept, year, get_class_name(class_name))
    return ''


def group_words(s):
    regex = []

    # Match a whole word:
    regex += [ur'\w+']

    # Match a single CJK character:
    regex += [ur'[\u4e00-\ufaff]']

    # Match one of anything else, except for spaces:
    regex += [ur'[^\s]']

    regex = "|".join(regex)
    r = re.compile(regex)

    return r.findall(s)


def search(request):
    q = request.GET.get('q', '')
    q = ' '.join(group_words(q))

    next_page = request.GET.get('next_page', '')

    #student_id = request.GET.get('student_id', '')
    if get_dept(q):
        courses = Department.objects.get(dept_name=get_dept(q)).required_course.all()
    else:
        courses = SearchQuerySet().filter(content=AutoQuery(q)).order_by('-hit')

    pager = Paginator(courses, 10)

    try:
        courses_page = pager.page(next_page)
    except PageNotAnInteger:
        courses_page = pager.page(1)
    except EmptyPage:
        courses_page = pager.page(pager.num_pages)


    courses_list = Course.objects.filter(pk__in=[c.pk for c in courses_page.object_list]). \
        values('id', 'no', 'eng_title', 'chi_title', 'note', 'objective',
               'time', 'teacher', 'room', 'credit', 'prerequisite', 'ge')

    result = {
        'total': courses.count(),
        'next': courses_page.next_page_number() if courses_page.has_next() else pager.num_pages,
        'courses': list(courses_list)
    }

    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))


@cache_page(60 * 60)
def syllabus(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'syllabus.html', {'course': course})


def hit(request, id):
    course = get_object_or_404(Course, id=id)
    course.hit += 1
    course.save()
    return HttpResponse('')
