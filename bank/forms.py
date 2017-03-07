from .models import Account
from .models import Bank
from .models import Customer
from django import forms
from .models import Transaction
from django.contrib.auth.models import User


class BankForm(forms.ModelForm):

    class Meta:
        model = Bank
        exclude = ['timestamp', 'updated']

    def clean_ifsc(self):
        data = self.cleaned_data['ifsc']
        if Bank.objects.all().filter(ifsc=data):
            raise forms.ValidationError("'%s' has already been taken" % data)
        return data

    def __init__(self, user, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['user'] = user
            del self.fields['user']

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = \
                self.fields[key].label
            self.fields[key].widget.attrs['id'] = self.fields[key].label


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['timestamp', 'updated']

    def __init__(self, user, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['disabled'] = True
        self.fields['bank'].widget.attrs['disabled'] = True

        if not user.is_superuser:
            self.fields['user'] = user
            del self.fields['user']

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = \
                self.fields[key].label
            self.fields[key].widget.attrs['id'] = self.fields[key].label


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ['timestamp', 'updated']

    def __init__(self, user, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['disabled'] = True
        self.fields['customer'].widget.attrs['disabled'] = True

        if not user.is_superuser:
            self.fields['user'] = user
            del self.fields['user']

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = \
                self.fields[key].label
            self.fields[key].widget.attrs['id'] = self.fields[key].label


class TransactionsForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ['timestamp', 'updated']

    def __init__(self, user, account_obj, *args, **kwargs):
        self.account_obj = account_obj
        super(TransactionsForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['disabled'] = True
        self.fields['account'].widget.attrs['disabled'] = True

        if not user.is_superuser:
            self.fields['user'] = user
            del self.fields['user']

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = \
                self.fields[key].label
            self.fields[key].widget.attrs['id'] = self.fields[key].label

    def clean_amount(self):
        data = self.cleaned_data['amount']
        account_obj = self.account_obj
        transaction_type = self.cleaned_data['transaction_type']

        if data < 0:
            raise forms.ValidationError('Amount can not be -ve . . .')

        elif transaction_type == 'Withdraw':
            if data > account_obj.balance:
                raise forms.ValidationError('Oops, Balance low...')

        return data


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username")
    email = forms.CharField(label="email")
    password1 = forms.CharField(label="password1")
    password2 = forms.CharField(label="password2")

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.all().filter(username=data):
            raise forms.ValidationError(
                "Username '%s' has already been taken" % data
            )
        return data

    def clean_password2(self):
        data = self.cleaned_data['password2']
        data_password = self.cleaned_data['password1']
        if data != data_password:
            raise forms.ValidationError("Password mismatch")
        return data
