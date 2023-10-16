from django.shortcuts import render


def index(request):
    return render(request, 'gorynych_app/index.html')