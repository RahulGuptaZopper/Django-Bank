from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Branch
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Bank
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Client
        fields = ['user_id','name','address','pan_card','aadhar_card']
    def create(self, validated_data):
        return Client.objects.create(**validated_data)

class AccountSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Account
        fields = ['user_id','account_type','bank']

class TransferSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Transfer
        fields = ['to_account','amount']

class TransactionsSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Transactions
        fields = ['amount','transaction_type']
