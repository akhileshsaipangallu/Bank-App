# Django
from django.contrib import admin

# local Django
from .models import Account
from .models import Bank
from .models import Customer
from .models import Transaction


class BankModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ifsc', 'branch', 'zip_code']
    list_display_links = ['name', 'ifsc']
    # list_filter = ['name']
    search_fields = ['name', 'ifsc', 'branch', 'zip_code', 'state', 'city']


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'bank']
    list_display_links = ['first_name', 'last_name']
    # list_filter = ['first_name']
    search_fields = ['first_name', 'last_name']


class AccountModelAdmin(admin.ModelAdmin):
    list_display = ['customer', 'account_number', 'account_type', 'balance']
    list_display_links = ['customer', 'account_number']
    list_filter = ['account_number']
    search_fields = ['customer', 'account_number']


class TransactionsModelAdmin(admin.ModelAdmin):
    list_display = ['account','transaction_type', 'updated']
    list_display_links = ['account']
    list_filter = ['transaction_type']
    search_fields = ['account', 'transaction_type', 'updated']

admin.site.register(Bank, BankModelAdmin)
admin.site.register(Customer, CustomerModelAdmin)
admin.site.register(Account, AccountModelAdmin)
admin.site.register(Transaction, TransactionsModelAdmin)
