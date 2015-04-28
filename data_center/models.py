from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Course database schema"""
    note            = models.TextField()
    object          = models.TextField()
    time            = models.TextField()
    no              = models.TextField()
    title           = models.TextField()
    teacher         = models.TextField()
    room            = models.TextField()
    credit          = models.IntegerField()
    limit           = models.IntegerField()
    prerequisite    = models.BooleanField(default=False)

    def __str__(self):
        return self.no

class Schedule(models.Model):
    """Many2ManySchedule"""
    owner = models.ForeignKey(User)
    select_course = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return "%s - %d" % (self.owner, self.id)
