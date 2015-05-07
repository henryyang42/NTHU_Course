from django.shortcuts import render

def table_index(request):
    return render(request, 'table.html')
