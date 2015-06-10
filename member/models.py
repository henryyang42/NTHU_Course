from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User)

    # Facebook field
    uuid = models.CharField('User ID', max_length=100)
    email = models.EmailField('Email')


    def __str__(self):
        return self.user.get_username()
