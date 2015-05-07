from django.shortcuts import render
from data_center.models import Course
from django.db.models import Q

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
