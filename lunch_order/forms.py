# coding: UTF-8
from django import forms


class OrderForm(forms.Form):
    dish = forms.CharField(required=True, max_length=100, label='Что купить:')
    byr = forms.IntegerField(required=False, label='Оплачено BYR:')
    byn = forms.FloatField(min_value=0, required=False, label='Оплачено BYN:')
    comment = forms.CharField(max_length=300, required=False, label='Комментарий:')
    name = forms.CharField(max_length=100, required=True, label='Кому:')
    email = forms.EmailField(required=True, label='E-mail:')
