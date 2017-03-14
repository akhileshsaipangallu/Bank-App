from rest_framework.decorators import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from bank.models import Bank
import serializers


class BankList(APIView):
    def get(self, request):
        bank_list = Bank.objects.all()
        bank_serializer = serializers.BankSerializer(bank_list, many=True)
        print bank_serializer
        return Response(bank_serializer.data)


class BankDetails(BankList):
    def get(self, request, ifsc):
        ifsc = ifsc.upper()
        bank_obj = get_object_or_404(Bank, ifsc=ifsc)
        bank_serializer = serializers.BankSerializer(bank_obj, many=False)
        return Response(bank_serializer.data)
