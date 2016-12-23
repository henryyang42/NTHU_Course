from django.shortcuts import render


def error404(request):
    return render(request, template_name='index/404.html')
