from django.shortcuts import render
from .service import game


def index(request):
    context = {'game': game}
    return render(request, 'gorynych_app/index.html', context=context)