from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def order(request):
    pass


def admin(request):
    pass
