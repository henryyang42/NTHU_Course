# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models


class Course(models.Model):
    """Course database schema"""
    no = models.CharField(max_length=20, blank=True)
    code = models.CharField(max_length=20, blank=True)
    eng_title = models.CharField(max_length=200, blank=True)
    chi_title = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    objective = models.CharField(max_length=80, blank=True)
    time = models.CharField(max_length=20, blank=True)
    time_token = models.CharField(max_length=20, blank=True)
    teacher = models.CharField(max_length=40, blank=True)  # Only save Chinese
    room = models.CharField(max_length=20, blank=True)
    credit = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    prerequisite = models.BooleanField(default=False, blank=True)

    ge = models.CharField(max_length=80, blank=True)

    hit = models.IntegerField(default=0)

    syllabus = models.TextField(blank=True)  # A html div

    def __str__(self):
        return self.no


class Department(models.Model):
    dept_name = models.CharField(max_length=20, blank=True)
    required_course = models.ManyToManyField(Course, blank=True)

    def __unicode__(self):
        return self.dept_name


class Announcement(models.Model):
    TAG_CHOICE = (
        ('Info', '公告'),
        ('Bug', '已知問題'),
        ('Fix', '問題修復'),
    )

    content = models.TextField(blank=True)
    time = models.DateTimeField(default=datetime.now)
    tag = models.CharField(max_length=10, choices=TAG_CHOICE, default='Info')

    def __unicode__(self):
        return '%s|%s' % (self.time, self.tag)
