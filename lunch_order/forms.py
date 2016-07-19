# coding: UTF-8
from django import forms


class OrderForm(forms.Form):
    dish = forms.CharField(required=True, min_length=1, max_length=100, label='Что купить:')
    byr = forms.IntegerField(required=False, min_value=0, label='Оплачено BYR:')
    byn = forms.FloatField(required=False, min_value=0, label='Оплачено BYN:')
    comment = forms.CharField(required=False, max_length=300, label='Комментарий:')
    name = forms.CharField(required=True, min_length=1, max_length=100, label='Кому:')
    email = forms.EmailField(required=True, min_length=1, max_length=100, label='E-mail:')
