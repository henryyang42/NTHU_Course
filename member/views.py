from django.shortcuts import render
from member.models import Member

def save_userdata(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            profile = Member.objects.get(user_id=user.id)
        except Member.DoesNotExist:
            profile = Member(user_id=user.id)
        profile.gender = response.get('gender')
        profile.link = response.get('link')
        profile.timezone = response.get('timezone')
        profile.department= '???????'
        profile.save()