from .models import Account
from .forms import AccountForm
from .models import Bank
from .forms import BankForm
from .models import Customer
from .forms import CustomerForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm
from django.shortcuts import render
from django.shortcuts import reverse
from .models import Transaction
from .forms import TransactionsForm
from django.contrib.auth.models import User


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('bank_list'))


@login_required
def about(request):
    context = {'user': request.user}
    return render(request, 'bank/about.html', context)


@login_required
def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            user.save()
            return HttpResponseRedirect(reverse('bank_list'))

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'bank/registration_form.html', context)


@login_required
def bank_add(request):
    user = request.user
    form_obj = BankForm(user)

    if request.method == 'POST':
        form_obj = BankForm(user, request.POST)

        if form_obj.is_valid():
            instance = form_obj.save()
            if not request.user.is_superuser:
                instance.user = request.user
                instance.save()
            return HttpResponseRedirect(reverse('bank_list'))

    context = {
        'bank_form': form_obj,
        'user': request.user,
    }
    return render(request, 'bank/bank_form.html', context)


@login_required
def bank_list(request):
    empty = False
    if request.user.is_superuser:
        query_set = Bank.objects.all()
    else:
        query_set = Bank.objects.filter(user=request.user)
    if not query_set:
        empty = True
    context = {
        'bank_obj': query_set,
        'empty': empty,
        'user': request.user,
    }
    return render(request, 'bank/bank_list.html', context)


@login_required
def bank_details(request, ifsc):
    empty = False
    if request.user.is_superuser:
        query_set = get_object_or_404(
            Bank,
            ifsc=ifsc
        )
    else:
        query_set = get_object_or_404(
            Bank,
            user=request.user,
            ifsc=ifsc
        )

    if not query_set:
        empty = True
    context = {
        'bank_obj': query_set,
        'empty': empty,
        'ifsc': ifsc,
        'user': request.user,
    }
    return render(request, 'bank/bank_details.html', context)


@login_required
def bank_delete(request, ifsc):
    if request.user.is_superuser:
        query_set = get_object_or_404(
            Bank,
            ifsc=ifsc
        )
        query_set.delete()
    return HttpResponseRedirect(reverse('bank_list'))


@login_required
def customer_list(request, ifsc):
    empty = False
    bank_one = None
    query_set = None

    try:
        if request.user.is_superuser:
            query_set = Customer.objects.filter(
                bank__ifsc=ifsc
            )
        else:
            check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
            query_set = Customer.objects.filter(
                user=request.user,
                bank__ifsc=ifsc
            )
        bank_one = query_set[0]
    except IndexError:
        empty = True
    finally:
        context = {
            'customer_obj': query_set,
            'bank_one': bank_one,
            'empty': empty,
            'ifsc': ifsc,
            'user': request.user,
        }
        return render(request, 'bank/customer_list.html', context)


@login_required
def customer_details(request, ifsc, first_name, last_name, id):
    if request.user.is_superuser:
        query_set = get_object_or_404(
            Customer,
            first_name=first_name,
            last_name=last_name,
            id=id
        )
    else:
        check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
        query_set = get_object_or_404(
            Customer,
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            id=id
        )
    context = {
        'customer_obj': query_set,
        'ifsc': ifsc,
        'first_name': first_name,
        'last_name': last_name,
        'id': id,
        'user': request.user,
    }
    return render(request, 'bank/customer_details.html', context)


@login_required
def customer_delete(request, ifsc, first_name, last_name, id):
    if request.user.is_superuser:
        query_set = get_object_or_404(
            Customer,
            first_name=first_name,
            last_name=last_name,
            id=id
        )
        query_set.delete()

    return HttpResponseRedirect(
        reverse(
            'customer_list',
            kwargs={
                'ifsc': ifsc
            }
        )
    )


@login_required
def customer_add(request, ifsc):
    user = request.user
    if request.user.is_superuser:
        bank_obj = get_object_or_404(
            Bank,
            ifsc=ifsc
        )
    else:
        check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
        bank_obj = get_object_or_404(
            Bank,
            user=request.user,
            ifsc=ifsc
        )
    form_obj = CustomerForm(
        user,
        initial={
            'bank': bank_obj.id,
            'user': bank_obj.user,
        }
    )

    if request.method == 'POST':
        form_obj = CustomerForm(user, request.POST)

        if form_obj.is_valid():
            instance = form_obj.save()
            instance.bank = bank_obj
            instance.user = bank_obj.user
            instance.save()
            return HttpResponseRedirect(
                reverse(
                    'customer_list',
                    kwargs={
                        'ifsc': ifsc,
                    }
                )
            )
    context = {
        'customer_form': form_obj,
        'user': request.user
    }
    return render(request, 'bank/customer_form.html', context)


@login_required
def account_list(request, ifsc, first_name, last_name, id):
    empty = False
    account_obj_one = None
    query_set = None
    try:
        if request.user.is_superuser:
            query_set = Account.objects.filter(
                customer__first_name=first_name,
                customer__last_name=last_name
            )
        else:
            check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
            query_set = Account.objects.filter(
                user=request.user,
                customer__first_name=first_name,
                customer__last_name=last_name
            )
        account_obj_one = query_set[0]
    except IndexError:
        empty = True
    finally:
        context = {
            'account_obj': query_set,
            'account_obj_one': account_obj_one,
            'empty': empty,
            'ifsc': ifsc,
            'first_name': first_name,
            'last_name': last_name,
            'id': id,
            'user': request.user,
        }
    return render(request, 'bank/account_list.html', context)


@login_required
def account_delete(request, ifsc, first_name, last_name, account_number, id):
    if request.user.is_superuser:
        query_set = get_object_or_404(
            Account,
            account_number=account_number,
        )
        query_set.delete()

    return HttpResponseRedirect(
        reverse(
            'account_list',
            kwargs={
                'ifsc': ifsc,
                'first_name': first_name,
                'last_name': last_name,
                'id': id,
            }
        )
    )


@login_required
def account_add(request, ifsc, first_name, last_name, id):
    user = request.user
    if user.is_superuser:
        customer_obj = get_object_or_404(
            Customer,
            first_name=first_name,
            last_name=last_name,
            id=id
        )
    else:
        check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
        customer_obj = get_object_or_404(
            Customer,
            user=user,
            first_name=first_name,
            last_name=last_name,
            id=id
        )
    form_obj = AccountForm(
        user,
        initial={
            'customer': customer_obj.id,
            'user': customer_obj.user,
        }
    )

    if request.method == 'POST':
        form_obj = AccountForm(user, request.POST)

        if form_obj.is_valid():
            instance = form_obj.save()
            instance.user = request.user
            instance.customer = customer_obj
            instance.user = customer_obj.user
            instance.save()
            return HttpResponseRedirect(
                reverse(
                    'account_list',
                    kwargs={
                        'ifsc': ifsc,
                        'first_name': first_name,
                        'last_name': last_name,
                        'id': id,
                    }
                )
            )

    context = {
        'account_form': form_obj,
        'user': user,
    }
    return render(request, 'bank/account_form.html', context)


@login_required
def transaction_list(request, ifsc, first_name, last_name, account_number, id):
    transaction_obj_one = None
    query_set = None
    empty = False

    try:
        if request.user.is_superuser:
            query_set = Transaction.objects.filter(
                account__account_number=account_number
            )
        else:
            check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
            query_set = Transaction.objects.filter(
                user=request.user,
                account__account_number=account_number
            )
        transaction_obj_one = query_set[0]

    except IndexError:
        empty = True

    finally:
        context = {
            'transaction_obj': query_set,
            'transaction_obj_one': transaction_obj_one,
            'ifsc': ifsc,
            'first_name': first_name,
            'last_name': last_name,
            'id': id,
            'account_number': account_number,
            'empty': empty,
            'user': request.user,
        }
        return render(request, 'bank/transaction_list.html', context)


@login_required
def transaction_add(request, ifsc, first_name, last_name, id, account_number):
    user = request.user
    if user.is_superuser:
        account_obj = get_object_or_404(
            Account,
            account_number=account_number
        )
    else:
        check_user = get_object_or_404(Bank, user=request.user, ifsc=ifsc)
        account_obj = get_object_or_404(
            Account,
            user=request.user,
            account_number=account_number
        )
    form_obj = TransactionsForm(
        user,
        account_obj,
        initial={
            'account': account_obj.account_number,
            'user': account_obj.user,
        }
    )

    if request.method == 'POST':
        form_obj = TransactionsForm(user, account_obj, request.POST)

        if form_obj.is_valid():
            if form_obj.cleaned_data.get('transaction_type') == 'Deposit':
                obj = get_object_or_404(
                    Account,
                    account_number=account_number
                )
                obj.balance += form_obj.cleaned_data.get('amount')
                obj.save()
                instance = form_obj.save()
                instance.user = account_obj.user
                instance.account = account_obj
                instance.save()
                return HttpResponseRedirect(
                    reverse(
                        'transaction_list',
                        kwargs={
                            'ifsc': ifsc,
                            'first_name': first_name,
                            'last_name': last_name,
                            'id': id,
                            'account_number': account_number,
                        }
                    )
                )

            elif form_obj.cleaned_data.get('transaction_type') == 'Withdraw':
                obj = get_object_or_404(
                    Account,
                    account_number=account_number
                )
                obj.balance -= form_obj.cleaned_data.get('amount')
                obj.save()
                instance = form_obj.save()
                instance.user = account_obj.user
                instance.account = account_obj
                instance.save()
                return HttpResponseRedirect(
                    reverse(
                        'transaction_list',
                        kwargs={
                            'ifsc': ifsc,
                            'first_name': first_name,
                            'last_name': last_name,
                            'id': id,
                            'account_number': account_number,
                        }
                    )
                )

    context = {
        'transaction_form': form_obj,
        'user': user,
    }
    return render(request, 'bank/transaction_form.html', context)
