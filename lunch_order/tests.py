# coding: UTF-8
from django.test import TestCase
from lunch_order.models import Orders
from views import count_total
from django.contrib.auth.models import User
from django.test import Client


class LunchOrderTest(TestCase):

    def test_ok_add_order(self):
        User.objects.create_superuser('admin_test', 'admin_test@admin.com', 'Qwerty123')
        data = {'dish': u'Рагу', 'byr': 50000, 'byn': 12.05, 'comment': u'Комментарий', 'name': u'Клиент', 'email': 'a@a.com'}
        self.client.post('/order/', data)
        q_data = Orders.objects.filter()
        self.assertEquals(q_data.count(), 1)
        order = q_data.get()
        self.assertEquals(order.dish, data['dish'])
        self.assertEquals(order.byn, data['byn'])
        self.assertEquals(order.byr, data['byr'])
        self.assertEquals(order.comment, data['comment'])
        self.assertEquals(order.name, data['name'])
        self.assertEquals(order.email, data['email'])

    def test_ok_count_total(self):
        User.objects.create_superuser('admin_test', 'admin_test@admin.com', 'Qwerty123')
        datas = [{'dish': u'Рагу', 'byr': 50000, 'byn': 12.05, 'comment': u'Комментарий', 'name': u'Клиент', 'email': 'a@a.com'},
                 {'dish': u'Рагу2', 'byn': 5.73, 'comment': u'Комментарий2', 'name': u'Клиент2', 'email': 'a2@a.com'},
                 {'dish': u'Рагу3', 'byr': 35000, 'comment': u'Комментарий3', 'name': u'Клиент3', 'email': 'a3@a.com'}]
        for data in datas:
            self.client.post('/order/', data)
        q_data = Orders.objects.filter()
        self.assertEquals(q_data.count(), 3)
        total = count_total(q_data)
        self.assertEquals(total, (26.28, 17.78, 85000))

    def test_ok_edit_order(self):
        User.objects.create_superuser('admin_test', 'admin_test@admin.com', 'Qwerty123')
        self.client.post('/login/', {'username': 'admin_test', 'password': 'Qwerty123'})
        data = {'dish': u'Рагу', 'byr': 50000, 'byn': 12.05, 'comment': u'Комментарий', 'name': u'Клиент', 'email': 'a@a.com'}
        self.client.post('/order/', data)
        data_post = {'dish': u'Рагу2', 'byr': 55000, 'byn': 1.05, 'comment': u'Комментарий2', 'name': u'Клиент2', 'email': 'a2@a.com', 'id': 1}
        self.client.post('/edit/', data_post)
        q_data = Orders.objects.filter().last()
        self.assertEquals(q_data.dish, data_post['dish'])
        self.assertEquals(q_data.byn, data_post['byn'])
        self.assertEquals(q_data.byr, data_post['byr'])
        self.assertEquals(q_data.comment, data_post['comment'])
        self.assertEquals(q_data.name, data_post['name'])
        self.assertEquals(q_data.email, data_post['email'])

    def test_ok_delete_order(self):
        self.admin = User.objects.create_superuser('admin_test', 'admin_test@admin.com', 'Qwerty123')
        self.client.post('/login/', {'username': 'admin_test', 'password': 'Qwerty123'})
        data = {'dish': u'Рагу', 'byr': 50000, 'byn': 12.05, 'comment': u'Комментарий', 'name': u'Клиент', 'email': 'a@a.com'}
        self.client.post('/order/', data)
        data_get = Orders.objects.filter().last()
        self.client.get('/delete/', {'id': data_get.id})
        q_data = Orders.objects.filter()
        self.assertEquals(q_data.count(), 0)