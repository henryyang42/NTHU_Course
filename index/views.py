from django.shortcuts import render

from data_center.models import Announcement


def index(request):
    announcements = Announcement.objects.all().order_by('-time')
    return render(request, 'index.html', {'announcements': announcements})
