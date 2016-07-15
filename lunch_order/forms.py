from django import forms


class OrderForm(forms.Form):
    dish = forms.CharField(required=True, max_length=100, label='Dish:')
    byr = forms.IntegerField(required=False, label='BYR paid:')
    byn = forms.FloatField(min_value=0, required=False, label='BYN paid:')
    comment = forms.CharField(max_length=300, required=False, label='Comment:')
    name = forms.CharField(max_length=100, required=True, label='Name:')
    email = forms.EmailField(required=True, label='E-mail:')
