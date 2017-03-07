from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(
        r'^register/$',
        views.register,
        name='register',
    ),
    url(r'^$', views.bank_list, name='bank_list'),
    url(r'^add/$', views.bank_add, name='bank_add'),
    url(
        r'^(?P<ifsc>\w+)/$',
        views.bank_details,
        name='bank_details'
    ),
    url(
        r'^(?P<ifsc>\w+)/delete/$',
        views.bank_delete,
        name='bank_delete'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/$',
        views.customer_list,
        name='customer_list'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/$',
        views.customer_details,
        name='customer_details'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/delete/$',
        views.customer_delete,
        name='customer_delete'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/add/$',
        views.customer_add,
        name='customer_add'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/accounts/$',
        views.account_list,
        name='account_list'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/accounts/add/$',
        views.account_add,
        name='account_add'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/accounts/(?P<account_number>\w+)/transactions/$',
        views.transaction_list,
        name='transaction_list'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/accounts/(?P<account_number>\w+)/transactions/delete/$',
        views.account_delete,
        name='account_delete'
    ),

    url(
        r'^(?P<ifsc>\w+)/customer/(?P<first_name>\w+)-(?P<last_name>\w+)-'
        r'(?P<id>\d+)/accounts/(?P<account_number>\w+)/transactions/add/$',
        views.transaction_add,
        name='transaction_add'
    ),
]
