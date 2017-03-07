from bank.models import Bank
from bank.models import Customer


count = input('Enter Count\n')
bank_ifsc = raw_input('Enter Bank ifsc\n')
customer_first_name = raw_input('Enter Customer first name Prefix\n')
customer_last_name = raw_input('Enter Customer last name Prefix\n')

for i in range(count):
    bank_obj = Bank.objects.all().get(ifsc=bank_ifsc)
    obj = Customer(
        bank=bank_obj,
        first_name='%s%d' % (customer_first_name, i),
        last_name='%s%d' % (customer_last_name, i),
        city='CITY%d' % i,
        state='STATE%d' % i,
        zip_code='100%d' % i
    )
    obj.save()
