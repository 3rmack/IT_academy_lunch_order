from django.shortcuts import render
from django.http import HttpResponse
from forms import OrderForm
from models import Orders


def index(request):
    return render(request, 'index.html')


def order(request):
    if request.method == 'POST':
        raw_data = OrderForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data
            Orders.objects.create(**data)
            return HttpResponse('ok')
        else:
            return HttpResponse('bad')
    else:
        order_f = OrderForm()
        order_f.dish()
        context = {'order_add_form': order_f}
        return render(request, 'order_add_form.html', context)


def admin(request):
    pass
