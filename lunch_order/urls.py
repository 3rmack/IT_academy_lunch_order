from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'order/', views.order, name='order'),
    url(r'admin_page/', views.admin, name='admin_page'),
    url(r'edit/', views.edit_order, name='edit'),
    url(r'delete/', views.delete_order, name='delete'),
    url(r'logout_success/', views.logout_success, name='logout_success'),
    url(r'logout/', 'django.contrib.auth.views.logout', {'next_page': '/logout_success/'}, name='logout'),
    url(r'login/', 'django.contrib.auth.views.login', name='login'),
    url(r'', views.index, name='index'),
]
