
from django.db import models
from django.conf import settings
# Create your models here.
from accounts.models import CustomUser

class Branch(models.Model) :
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    branch_code = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Bank(models.Model) :
    name = models.CharField(max_length=250)
    Branch = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Client(models.Model) :
    user_id=models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    pan_card = models.CharField(max_length=50,unique=True)
    aadhar_card = models.PositiveBigIntegerField(default = 0,unique=True)

    def __str__(self) -> str:
        return self.name

class Account(models.Model) :
    user_id=models.PositiveIntegerField(default=0)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    open_date = models.DateTimeField(auto_now=True)
    deposit = models.PositiveIntegerField(default=0)
    credit_card = models.PositiveBigIntegerField(default=0)
    debit_card = models.PositiveBigIntegerField(default=0)

    Savings ='s'
    Current = 'c'
    ACCOUNT_TYPE = [(Savings,'Savings'),(Current,'Current')]
    account_type= models.CharField(max_length=2,choices=ACCOUNT_TYPE,default=Savings)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE)

class Transfer(models.Model) :
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    to_account = models.CharField(max_length=20)
    amount = models.FloatField(default=0)
    transfer_date = models.DateTimeField(auto_now=True)
    from_balance = models.PositiveIntegerField(default=0)
    to_balance= models.PositiveIntegerField(default=0)

class Transactions(models.Model) :
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    balance=models.FloatField(default=0)


    withdraw = 'WITHDRAW'
    deposit = 'DEPOSIT'
    TRANSACTION_TYPE =[(withdraw,'WITHDRAW'),(deposit,'DEPOSIT')]
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE,default=deposit) 
    transaction_date=models.DateTimeField(auto_now=True)

    






