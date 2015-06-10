from member.models import Member


def save_userdata(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            profile = Member.objects.get(user_id=user.id)
        except Member.DoesNotExist:
            profile = Member(user_id=user.id)
        profile.uuid = response.get('id')
        profile.email = response.get('email')
        profile.save()
