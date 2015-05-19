import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from data_center.models import Course
from django.db.models import Q
from django.views.decorators.cache import cache_page

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
# Create your views here.

def search(request):
    q = request.GET.get('q', '')
    next_page = request.GET.get('next_page', '')

    courses = SearchQuerySet().filter(content=AutoQuery(q))
    courses = Course.objects.filter(pk__in=[c.pk for c in courses]). \
        values('id', 'no', 'eng_title', 'chi_title', 'note', 'objective',
            'time', 'teacher', 'room', 'credit', 'prerequisite').order_by('-hit')

    pager = Paginator(courses, 10)

    try:
        courses_page = pager.page(next_page)
    except PageNotAnInteger:
        courses_page = pager.page(1)
    except EmptyPage:
        courses_page = pager.page(pager.num_pages)

    result = {
        'total': courses.count(),
        'next': courses_page.next_page_number() if courses_page.has_next() else pager.num_pages,
        'courses': list(courses_page.object_list)
    }

    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))


@cache_page(60 * 60)
def syllabus(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'syllabus.html', {'course': course})


@cache_page(60 * 60)
def hit(request, id):
    course = get_object_or_404(Course, id=id)
    course.hit += 1
    course.save()
    return HttpResponse('')
