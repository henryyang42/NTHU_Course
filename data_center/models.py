# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.http import urlquote

attachment_url_format = (
    'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/'
    +'output/6_6.1_6.1.12/%s.pdf')


class Course(models.Model):
    """Course database schema"""
    no = models.CharField(max_length=20, unique=True, db_index=True)
    code = models.CharField(max_length=20, blank=True)
    eng_title = models.CharField(max_length=200, blank=True)
    chi_title = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    objective = models.CharField(max_length=80, blank=True)
    time = models.CharField(max_length=20, blank=True)
    time_token = models.CharField(max_length=20, blank=True)
    teacher = models.CharField(max_length=40, blank=True)  # Only save Chinese
    room = models.CharField(max_length=80, blank=True)
    credit = models.IntegerField(default=0)
    limit = models.IntegerField(default=0)
    prerequisite = models.BooleanField(default=False, blank=True)
    ys = models.CharField(max_length=10, blank=True)

    ge = models.CharField(max_length=80, blank=True)

    hit = models.IntegerField(default=0)

    syllabus = models.TextField(blank=True)  # pure text
    has_attachment = models.BooleanField(default=False)  # has pdf

    def __str__(self):
        return self.no

    @property
    def attachment_url(self):
        return attachment_url_format % urlquote(self.no)


class Department(models.Model):
    dept_name = models.CharField(max_length=20, blank=True)
    required_course = models.ManyToManyField(Course, blank=True)
    ys = models.CharField(max_length=10, blank=True)

    def __str__(self):
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

    def __str__(self):
        return '%s|%s' % (self.time, self.tag)


class FlatPrerequisite(models.Model):
    '''
    store rendered prerequisite in the database
    alternative: django.contrib.flatpage
    '''
    updated_at = models.DateTimeField(auto_now=True)
    html = models.TextField()

    @classmethod
    def update_html(cls, html):
        if cls.objects.exists():
            ins = cls.objects.get()
            ins.html = html
            ins.save()
            return ins
        else:
            return cls.objects.create(html=html)
