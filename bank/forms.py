from .models import Account
from .models import Bank
from .models import Customer
from django import forms
from .models import Transaction
from django.contrib.auth.models import User


def string_validation(data, field_name):
    for char in data:
        if not char.isalpha():
            raise forms.ValidationError(
                "Enter a valid %s name" % field_name
            )


class BankForm(forms.ModelForm):

    class Meta:
        model = Bank
        exclude = ['timestamp', 'updated']

    def clean_name(self):
        name = self.cleaned_data['name']
        string_validation(name, 'Bank')
        return name

    def clean_branch(self):
        branch = self.cleaned_data['branch']
        string_validation(branch, 'Branch')
        return branch

    def clean_city(self):
        city = self.cleaned_data['city']
        string_validation(city, 'City')
        return city

    def clean_state(self):
        state = self.cleaned_data['state']
        string_validation(state, 'State')
        return state

    def clean_ifsc(self):
        ifsc = self.cleaned_data['ifsc']
        if Bank.objects.filter(ifsc=ifsc):
            raise forms.ValidationError("'%s' has already been taken" % ifsc)
        return ifsc

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

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        string_validation(first_name, 'First')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        string_validation(last_name, 'Last')
        return last_name

    def clean_city(self):
        city = self.cleaned_data['city']
        string_validation(city, 'City')
        return city

    def clean_state(self):
        state = self.cleaned_data['state']
        string_validation(state, 'State')
        return state

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

    def clean_balance(self):
        balance = self.cleaned_data['balance']
        if balance < 0:
            raise forms.ValidationError('Balance cannot be -ve')
        return balance

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
            raise forms.ValidationError('Amount can not be -ve')

        elif transaction_type == 'Withdraw':
            if data > account_obj.balance:
                raise forms.ValidationError('Oops, Balance low')

        return data


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username")
    email = forms.CharField(label="email")
    password1 = forms.CharField(label="password1")
    password2 = forms.CharField(label="password2")

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data):
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
