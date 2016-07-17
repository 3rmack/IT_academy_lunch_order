from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'order', views.order, name='order'),
    url(r'admin_page', views.admin, name='admin_page'),
    url(r'edit', views.edit_order, name='edit'),
    url(r'delete', views.delete_order, name='delete'),
    url(r'', views.index, name='index'),
]
