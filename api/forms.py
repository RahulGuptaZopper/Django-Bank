
from django import forms
from .models import *

class CreateClientForm(forms.ModelForm) :
    class Meta:
        model = Client
        fields = ['name','address','pan_card','aadhar_card']

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Client Full Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder' : 'Client Address'}),
            'pan_card': forms.TextInput(attrs={'class' : 'form-control','palceholder' : 'Client Pan Card'}),
            'aadhar_card' : forms.NumberInput(attrs={'class' : 'form-control','palceholder' : 'Client Aadhar Card'}),
        }

class CreateAccountForm(forms.ModelForm) :
    class Meta:
        model= Account
        fields = ['account_type','bank']

        widgets = {
            'account_type' : forms.Select(attrs={'class' : 'form-control','placeholder' : 'Account Type'}),
            'bank' : forms.Select(attrs={'class' : 'form-control','placeholder' : 'Bank Select'}),
            }

class TransactionForm(forms.ModelForm) :
    class Meta :
        model = Transactions
        fields = ['amount','transaction_type']

        widgets = {
            'transaction_type' : forms.Select(attrs={'class' : 'form-control','placeholder' : 'Choice'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control','placeholder' : 'Amount'}),
        }


class TransferForm(forms.ModelForm) :
    class Meta :
        model = Transfer
        fields = ['to_account','amount']

        widgets = {
            'to_account' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Reciever'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control','placeholder' : 'Amount'})
        } 