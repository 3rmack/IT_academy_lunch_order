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


def send_email(recipient, order, order_old=None):
    subject = ''
    sender = User.objects.filter(is_superuser=True).first().email

    if order_old:
        if not order_old.byn:
            order_old.byn = ''
        if not order_old.byr:
            order_old.byr = ''
    if not order.byn:
        order.byn = ''
    if not order.byr:
        order.byr = ''
    body = u'Что купить: {0}\n' \
           u'Кому: {1}\n' \
           u'Оплачено BYN: {2}\n' \
           u'Оплачено BYR: {3}\n' \
           u'Комментарий: {4}'.format(order.dish, order.name, order.byn, order.byr, order.comment)
    recipients = [order.email]

    if recipient == 'user':
        subject = 'Ваш заказ был изменен'
        body = u'Старый заказ\n' \
               u'Что купить: {0}\n' \
               u'Кому: {1}\n' \
               u'Оплачено BYN: {2}\n' \
               u'Оплачено BYR: {3}\n' \
               u'Комментарий: {4}\n' \
               u'E-mail: {5}\n' \
               u'\n' \
               u'Новый заказ\n' \
               u'Что купить: {6}\n' \
               u'Кому: {7}\n' \
               u'Оплачено BYN: {8}\n' \
               u'Оплачено BYR: {9}\n' \
               u'Комментарий: {10}\n' \
               u'E-mail: {11}'.format(order_old.dish, order_old.name, order_old.byn, order_old.byr, order_old.comment, order_old.email,
                                      order.dish, order.name, order.byn, order.byr, order.comment, order.email)

    elif recipient == 'admin':
        subject = u'Новый заказ'
        recipients = [sender]
    elif recipient == 'delete':
        subject = u'Ваш заказ был удален'

    send_mail(subject, body, sender, recipients)


def check_time():
    time_notify_admin = time(13, 00)
    time_stop_work = time(15, 00)
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
            context = {'message': u'Заказ успешно добавлен'}
            return render(request, 'order_success.html', context)
        else:
            context = {'message': u'Ощибка. Вы ввели неверные данные'}
            return render(request, 'order_success.html', context)
    else:
        order_f = OrderForm()
        message = ''
        disable_submit = False

        if check_time() == 'stop':
            message = u'Время приема заказов истекло. Ваш заказ не будет принят.'
            disable_submit = True
            for field in order_f.fields:
                order_f.fields[field].widget.attrs['disabled'] = True

        context = {'order_add_form': order_f, 'message': message, 'disable_submit': disable_submit}
        return render(request, 'order_add_form.html', context)


@login_required(login_url='/login/')
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
        order_old = Orders.objects.get(id=order_to_edit['id'])
        order = Orders.objects.get(id=order_to_edit['id'])
        order.dish = order_to_edit['dish']
        order.name = order_to_edit['name']

        if order_to_edit['byn'] == '':
            order.byn = None
        else:
            order.byn = order_to_edit['byn']

        if order_to_edit['byr'] == '':
            order_old.byr = None
        else:
            order.byr = order_to_edit['byr']

        order.comment = order_to_edit['comment']
        order.email = order_to_edit['email']
        order.save()
        send_email('user', order, order_old=order_old)
        return render(request, 'edit_success.html', {'message': 'Edit success'})
    else:
        order_id = request.GET.get('id')
        order_to_edit = Orders.objects.get(id=order_id)
        context = {'order_to_edit': order_to_edit}
        return render(request, 'order_edit_form.html', context)


@login_required(login_url='/accounts/login/')
def delete_order(request):
    order_to_delete_id = request.GET.get('id')
    order = Orders.objects.get(id=order_to_delete_id)
    send_email('delete', order)
    order.delete()
    return render(request, 'edit_success.html', {'message': 'Order deleted'})


def logout_success(request):
    return render(request, 'logout_success.html', {'message': 'Вы успешно вышли из системы'})
