# -*- coding: utf-8 -*-
import json
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from data_center.models import Course, Department
from data_center.const import DEPT_CHOICE, GEC_CHOICE, \
    GE_CHOICE, CLASS_NAME_MAP, DEPT_MAP
from django.views.decorators.cache import cache_page
from django import forms

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery


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
    result = {}
    q = request.GET.get('q', '')
    q = ' '.join(group_words(q))
    page = request.GET.get('page', '')
    size = request.GET.get('size', '')
    code = request.GET.get('code', '')
    page_size = size or 10

    if get_dept(q):
        courses = Department.objects.get(
            dept_name=get_dept(q)).required_course.all()
        if courses:
            result['type'] = 'required'
            page_size = courses.count()
    else:
        courses = SearchQuerySet().filter(content=AutoQuery(q))
        if code:
            courses = courses.filter(code=code)
        if code in ['GE', 'GEC']:
            core = request.GET.get(code.lower(), '')
            if core:
                courses = Course.objects.filter(pk__in=[c.pk for c in courses])
                courses = courses.filter(ge__contains=core)

    paginator = Paginator(courses, page_size)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        courses_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        courses_page = paginator.page(paginator.num_pages)

    courses_list = Course.objects. \
        filter(pk__in=[c.pk for c in courses_page.object_list]). \
        values('id', 'no', 'eng_title', 'chi_title', 'note', 'objective',
               'time', 'teacher', 'room', 'credit', 'prerequisite', 'ge')

    result['total'] = courses.count()
    result['page'] = courses_page.number
    result['courses'] = list(courses_list)
    result['page_size'] = page_size

    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))


@cache_page(60 * 60)
def syllabus(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'syllabus.html',
                  {'course': course, 'syllabus_path': request.path})


def hit(request, id):
    course = get_object_or_404(Course, id=id)
    course.hit += 1
    course.save()
    return HttpResponse('')


class CourseSearchForm(forms.Form):
    q = forms.CharField(label='關鍵字', required=False)
    code = forms.ChoiceField(label='開課代號', choices=DEPT_CHOICE, required=False)
    ge = forms.ChoiceField(label='向度', choices=GE_CHOICE, required=False)
    gec = forms.ChoiceField(label='向度', choices=GEC_CHOICE, required=False)


def table(request):
    render_data = {}
    render_data['search_filter'] = CourseSearchForm(request.GET)
    return render(request, 'table.html', render_data)
