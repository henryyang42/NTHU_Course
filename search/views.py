# -*- coding: utf-8 -*-
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from data_center.models import Course, Department
from data_center.const import DEPT_CHOICE, GEC_CHOICE, GE_CHOICE
from django.views.decorators.cache import cache_page
from django import forms

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery


def group_words(s):
    """Split Chinese token for better search result"""
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
    dept_required = request.GET.get('dept_required', '')
    sortby_param = request.GET.get('sort', '')
    reverse_param = request.GET.get('reverse', '')

    page_size = size or 10
    sortby = sortby_param or 'time_token'
    reverse = True if reverse_param == 'true' else False
    rev_sortby = '-' + sortby if reverse else sortby

    courses = SearchQuerySet()

    if dept_required:
        try:
            courses = Department.objects.get(
                dept_name=dept_required).required_course.all()
        except:
            pass
        if courses:
            result['type'] = 'required'
            page_size = courses.count()
    else:
        courses = courses.filter(content=AutoQuery(q))
        if code:
            courses = courses.filter(code__contains=code)

        if courses.count() > 300:
            return HttpResponse('TMD')  # Too many detail

        courses = Course.objects.filter(pk__in=[c.pk for c in courses])
        if code in ['GE', 'GEC']:
            core = request.GET.get(code.lower(), '')
            if core:
                courses = courses.filter(ge__contains=core)

    courses = courses.order_by(rev_sortby)
    paginator = Paginator(courses, page_size)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        courses_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        courses_page = paginator.page(paginator.num_pages)

    courses_list = courses_page.object_list. \
        values('id', 'no', 'eng_title', 'chi_title', 'note', 'objective',
               'time', 'time_token', 'teacher', 'room', 'credit',
               'prerequisite', 'ge', 'code')

    result['total'] = courses.count()
    result['page'] = courses_page.number
    result['courses'] = list(courses_list)
    result['page_size'] = page_size

    return JsonResponse(result)


@cache_page(60 * 60)
def syllabus(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'syllabus.html',
                  {'course': course, 'syllabus_path': request.path})


def course_manipulation(request, id):
    """ Use this `course_manipulation` function to record the course """
    if request.user.is_authenticated():
        course = get_object_or_404(Course, id=id)

        if request.method == 'PUT':
            request.user.member.courses.add(course)
        elif request.method == 'DELETE':
            request.user.member.courses.remove(course)

    return JsonResponse('')


def courses_status(request):
    result = {}
    result['total'] = 0
    if request.user.is_authenticated():
        courses_list = request.user.member.courses. \
            values('id', 'no', 'eng_title', 'chi_title', 'note', 'objective',
                   'time', 'time_token', 'teacher', 'room', 'credit',
                   'prerequisite', 'ge', 'code')
        result['total'] = courses_list.count()
        result['courses'] = list(courses_list)

    return JsonResponse(result)


def generate_dept_required_choice():
    choices = (('', '---'),)
    departments = Department.objects.all()
    for department in departments:
        dept_name = department.dept_name
        year = {'104': '一年級', '103': '二年級', '102': '三年級', '101': '四年級'}. \
            get(dept_name[4:7], '')
        degree = {'B': '大學部', 'D': '博士班', 'M': '碩士班', 'P': '專班'}. \
            get(dept_name[7], '')
        chi_dept_name = degree

        if dept_name[7] == 'B':
            chi_dept_name += year
            chi_dept_name += {'BA': '清班', 'BB': '華班', 'BC': '梅班'}. \
                get(dept_name[7:], '')

        choices += ((dept_name, chi_dept_name),)
    return sorted(choices)


class CourseSearchForm(forms.Form):
    DEPT_REQUIRED_CHOICE = generate_dept_required_choice()
    q = forms.CharField(label='關鍵字', required=False)
    code = forms.ChoiceField(label='開課代號', choices=DEPT_CHOICE, required=False)
    ge = forms.ChoiceField(label='向度', choices=GE_CHOICE, required=False)
    gec = forms.ChoiceField(label='向度', choices=GEC_CHOICE, required=False)
    dept_required = forms.ChoiceField(
        label='必選修', choices=DEPT_REQUIRED_CHOICE, required=False)


def table(request):
    render_data = {}
    render_data['search_filter'] = CourseSearchForm(request.GET)
    return render(request, 'table.html', render_data)
