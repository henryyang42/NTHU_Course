from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User)
    getnder = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_username()