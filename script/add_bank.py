from bank.models import Bank

count = input('Enter Count\n')
name = raw_input('Enter Bank name Prefix\n')
ifsc = raw_input('Enter IFSC Prefix\n')

for i in range(count):
    obj = Bank(
        name='%s %d' % (name, i),
        ifsc='%s%d' % (ifsc, i),
        branch='BRANCH%d' % i,
        city='CITY%d' % i,
        state='STATE%d' % i,
        zip_code='100%d' % i
    )
    obj.save()
