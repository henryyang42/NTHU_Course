from django.shortcuts import render, get_object_or_404
from data_center.models import Course
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.

def search(request):
    q = request.GET.get('q', '')

    courses = Course.objects.filter(
        Q(no__icontains=q) |
        Q(time__icontains=q) |
        Q(eng_title__icontains=q) |
        Q(chi_title__icontains=q) |
        Q(teacher__icontains=q)
    ).distinct()[:50]

    return render(request, 'search.html', {'courses': courses})


def syllabus(request, id):
    course = get_object_or_404(Course, id=id)
    return HttpResponse(course.syllabus)
