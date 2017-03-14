from __future__ import unicode_literals
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

ACCOUNT_TYPE = (
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)
TRANSACTION_TYPE = (
    ('Deposit', 'Deposit'),
    ('Withdraw', 'Withdraw'),
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Bank(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=120)
    ifsc = models.CharField(max_length=20, unique=True, null=False)
    branch = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_absolute_url(self):
        return reverse(
            'bank_details',
            kwargs={
                'ifsc': self.ifsc,
            }
        )

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_absolute_url(self):
        return reverse(
            'customer_details',
            kwargs={
                'first_name': self.first_name,
                'last_name': self.last_name,
                'id': self.id,
                'ifsc': self.bank.ifsc,
            }
        )

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Account(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    account_number = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    balance = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return '% d' % (self.account_number,)


class Transaction(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE
    )
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.transaction_type
