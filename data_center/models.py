from django.db import models

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
