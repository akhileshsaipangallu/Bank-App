# third-party
from rest_framework import serializers

# local Django
from bank.models import Bank


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        exclude = ['id', 'user', 'timestamp', 'updated']
