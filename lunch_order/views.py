# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from forms import OrderForm
from models import Orders
from django.utils import timezone
from datetime import time


def index(request):
    return render(request, 'index.html')


def send_email(recipient, order):
    sender = User.objects.filter(is_superuser=True).first().email
    if recipient == 'user':
        subject = 'Your lunch order modified'
        body = u'Что купить: {0}\nКомментарий: {1}'.format(order.dish, order.comment)
        recipients = [order.email]
        send_mail(subject, body, sender, recipients)
    elif recipient == 'admin':
        subject = 'New lunch order'
        body = u'Что купить: {0}\nКому: {1}\nКомментарий: {2}'.format(order.dish, order.name, order.comment)
        recipients = [sender]
        send_mail(subject, body, sender, recipients)


def check_time():
    time_notify_admin = time(21, 00)
    time_stop_work = time(23, 00)
    time_now = timezone.localtime(timezone.now()).time()
    if time_now > time_stop_work:
        return 'stop'
    elif time_notify_admin < time_now < time_stop_work:
        return 'notify'
    else:
        return 'proceed'


@csrf_exempt
def order(request):
    if request.method == 'POST':
        raw_data = OrderForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data
            order = Orders.objects.create(**data)
            if check_time() == 'notify':
                send_email('admin', order)
                # print 'notify'
            context = {'message': 'Your lunch order successfully added'}
            return render(request, 'order_success.html', context)
        else:
            context = {'message': 'Lunch order failed. Looks like you input something not correct'}
            return render(request, 'order_success.html', context)
    else:
        order_f = OrderForm()
        message = ''
        disable_submit = False

        if check_time() == 'stop':
            message = 'Order time expired. Your order will not be accepted.'
            disable_submit = True
            for field in order_f.fields:
                order_f.fields[field].widget.attrs['disabled'] = True

        context = {'order_add_form': order_f, 'message': message, 'disable_submit': disable_submit}
        return render(request, 'order_add_form.html', context)


@login_required(login_url='/accounts/login/')
def admin(request):
    orders = Orders.objects.filter()
    total_byn = 0
    total_byr = 0
    for order in orders:
        if order.byn:
            total_byn += order.byn
        if order.byr:
            total_byr += order.byr
    total = total_byn + float(total_byr) / 10000
    context = {'orders': orders, 'total_byr': total_byr, 'total_byn': total_byn, 'total': total}
    return render(request, 'admin.html', context)


@csrf_exempt
@login_required(login_url='/accounts/login/')
def edit_order(request):
    if request.method == 'POST':
        order_to_edit = request.POST
        order = Orders.objects.get(id=order_to_edit['id'])
        order.dish = order_to_edit['dish']
        order.comment = order_to_edit['comment']
        order.save()
        send_email('user', order)
        return render(request, 'edit_success.html', {'message': 'Edit success'})
    else:
        order_id = request.GET.get('id')
        order_to_edit = Orders.objects.get(id=order_id)
        context = {'order_to_edit': order_to_edit}
        return render(request, 'order_edit_form.html', context)


@login_required(login_url='/accounts/login/')
def delete_order(request):
    order_to_delete_id = request.GET.get('id')
    Orders.objects.get(id=order_to_delete_id).delete()
    return render(request, 'edit_success.html', {'message': 'Order deleted'})
