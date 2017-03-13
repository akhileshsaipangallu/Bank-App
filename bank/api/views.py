from rest_framework.decorators import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from bank.models import Bank
import serializers


class BankList(APIView):
    def get(self, request):
        if request.user.is_authenticated():
            bank_list = Bank.objects.all()
            bank_serializer = serializers.BankSerializer(bank_list, many=True)
            return Response(bank_serializer.data)
        else:
            return Response(
                status=400,
                data='Permission Denied',
            )


class BankDetails(BankList):
    def get(self, request, ifsc):
        if request.user.is_authenticated():
            ifsc = ifsc.upper()
            bank_obj = get_object_or_404(Bank, ifsc=ifsc)
            bank_serializer = serializers.BankSerializer(bank_obj, many=False)
            return Response(bank_serializer.data)
        else:
            return Response(
                status=400,
                data='Permission Denied',
            )
