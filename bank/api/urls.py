from django.conf.urls import url
import views


urlpatterns = [
    url(r'^bank_list/$', views.BankList.as_view(), name='bank_list'),
    url(
        r'^bank-(?P<ifsc>\w+)/$',
        views.BankDetails.as_view(),
        name='bank_details',
    ),
]
