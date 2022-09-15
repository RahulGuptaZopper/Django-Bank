from http import client
from time import timezone
from urllib import response
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from django.views import generic
from django.template import loader

import os, pathlib,random,mimetypes

from .models import *
from .serializer import *
from .forms import *
from accounts.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer,HTMLFormRenderer
from rest_framework.decorators import permission_classes
from rest_framework import permissions  

class IndexView(APIView) :
    template_name = 'api/index.html'
    def get(self,request) :
        return Response()
#--------------------------------------------Branch Views-----------------------------------------------
class BranchesAPIView(APIView) :
    template_name = "api/branches.html" 
    renderer_classes = [TemplateHTMLRenderer]
    def get(self,request) :
        queryset = Branch.objects.all()
        return Response({'branch_list':queryset})

# class BranchDetailAPIView(APIView) :
#     template_name = 'api/branch.html'
#     renderer_classes = [TemplateHTMLRenderer]
#     def get(self, request,*args,**kwargs):
#         pk =self.kwargs.get('pk')
#         branch = get_object_or_404(Branch,pk)
#         serializer = BranchSerializer(branch)
#         return Response({'serializer' : serializer,"branch" : branch})

#----------------------------------------------Bank Views------------------------------------------------
class BanksAPIView(APIView) :
    template_name = "api/banks.html" 
    renderer_classes = [TemplateHTMLRenderer]
    def get(self,request) :
        queryset = Bank.objects.all() 
        return Response({'bank_list' : queryset})

# class BankDetailAPIView(APIView) :
#     template_name = "api/bank.html"
#     renderer_classes = [TemplateHTMLRenderer]
#     def get(self, request,*args,**kwargs):
#         pk =self.kwargs.get('pk')
#         bank = get_object_or_404(Bank,pk)
#         serializer = BankSerializer(bank)
#         return Response({'serializer' : serializer,"bank" : bank})


#--------------------------------------------Client Views-------------------------------------------------------


class UserListView(generics.ListAPIView) :
    """ Renders Client Details for currently logged in user
        If Client not linked 
        Then redirects to the create client link
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/clients.html'
    def get(self, request) :
        url =f"http://127.0.0.1:8000/api/create_client/"
        print(request.user.id)
        if Client.objects.filter(user_id=request.user.id).exists():
            client=get_object_or_404(Client,user_id=request.user.id)
            return Response({"client" : client})
        return HttpResponseRedirect(redirect_to=url)

class CreateClientAPIView(generics.CreateAPIView) :
    """
    Generates new client for the logged in user
    Adds data field user_id as the id of currently logged in user
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/createClient.html'

    def get(self,request,*args,**kwargs) : 
        serializer = ClientSerializer()
        form = CreateClientForm
        return Response({'serializer': serializer,'form':form})

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid() : 
            # name = serializer.validated_data.get('name')
            # address = serializer.validated_data.get('address')
            # pan_card = serializer.validated_data.get('pan_card')
            # aadhar_card = serializer.validated_data.get('aadhar_card')
            serializer.save(user_id=request.user.id)
            url=f'http://127.0.0.1:8000/api/client/'
            return HttpResponseRedirect(redirect_to=url)
        return HttpResponse("Aadhar and Pan Should be unique")

class UpdateClientAPIView(generics.RetrieveUpdateAPIView) :
    """
    Retrieves the client for current logged in user
    and generates a form for updating fields 
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/updateClient.html'

    def get(self, request) :
        client = Client.objects.get(user_id=request.user.id)
        serializer = ClientSerializer(client)
        form=CreateClientForm
        return Response({'serializer' : serializer,'form':form,"client" : client})

    def post(self, request):
        client = get_object_or_404(Client, user_id=request.user.id)
        serializer = ClientSerializer(client, data=request.data)
        if not serializer.is_valid():
            return HttpResponse("Aaadhar and Pan Card should be different for different users")
        serializer.save()
        url = f'http://127.0.0.1:8000/api/client/'
        return HttpResponseRedirect(redirect_to=url)

class DownloadClientAPIView(generics.ListAPIView) :
    """
    Creates a client detail file in txt format 
    which is downloadable
    """
    def get(self, request) :
        client = get_object_or_404(Client,user_id=request.user.id)
        serializer = ClientSerializer(client)

        Client_file = f"{client.name}.txt"
        file = pathlib.Path(Client_file)
        if file.exists ():
            os.remove(Client_file)  #delete if file already present create new file

        data = f"Customer Detail\n-------------------------------------------\n\
        Customer Name: {client.name}\n\
        Pan Number : {client.pan_card}\n\
        Aadhar Number : {client.aadhar_card}\n\
        Address : {client.address}"
        
        outfile = open('newaccounts.txt','w+')
        outfile.write(data)
        outfile.close()
        os.rename('newaccounts.txt', Client_file)

        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)

        # Define the full file path
        filepath = BASE_DIR + '/' + Client_file
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % Client_file
        return response
#--------------------------------------------Account Views------------------------------------------------------

class AccountUserListView(generics.ListAPIView) :
    """
     Renders Account Details for currently logged in user
        If Account not linked 
        Then redirects to the create account link
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/accounts.html'
    def get(self, request) :
        url =f"http://127.0.0.1:8000/api/create_account/"
        if Account.objects.filter(user_id=request.user.id).exists():
            account=get_object_or_404(Account,user_id=request.user.id)
            return Response({"account" : account})
        return HttpResponseRedirect(redirect_to=url)



class CreateAccountAPIView(generics.CreateAPIView) :

    """
    Generates new client for the logged in user
    Adds data field user_id as the id of currently logged in user
    """
    serializer_class = AccountSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name='api/createAccount.html'

    def get(self,request) :
        serializer= AccountSerializer
        form=CreateAccountForm
        return Response({'serializer' : serializer,'form' : form})

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid() :
            client =Client.objects.get(user_id=request.user.id)
            client_name = client.name[:3]
            number=client_name + str(random.randint(1000000000,9999999999))
            credit_card = random.randint(1000000000,9999999999)
            debit_card = random.randint(1000000000,9999999999)
            serializer.save(user_id=request.user.id,number=number,credit_card=credit_card,debit_card=debit_card,client=client)
            url = f'http://127.0.0.1:8000/api/accounts/'
            return HttpResponseRedirect(redirect_to=url)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class UpdateAccountAPIView(APIView) :
    """
    Retrieves the account for current logged in user
    and generates a form for updating fields 
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/updateAccount.html'

    def get(self, request) :
        account = get_object_or_404(Account,user_id=request.user.id)
        serializer = AccountSerializer(account)
        form=CreateAccountForm
        return Response({'serializer' : serializer,'form':form,"account" : account})

    def post(self, request):
        account = get_object_or_404(Account, user_id=request.user.id)
        serializer = AccountSerializer(account, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        url=f'http://127.0.0.1:8000/api/accounts/'
        return HttpResponseRedirect(redirect_to=url)

class DownloadAccountAPIView(generics.ListAPIView) :

    """
    Creates a account detail file in txt format
    which is downloadable
    """
    def get(self, request):
        account = get_object_or_404(Account,user_id=request.user.id)
        serializer = AccountSerializer(account)

        

        Account_file = f"{account.client.name}_account.txt"
        file = pathlib.Path(Account_file)
        if file.exists ():
            os.remove(Account_file)  #delete if file already present create new file

        data = f"Account Detail\n-------------------------------------------\n\
        Account Holder: {account.client.name}\n\
        Account Number: {account.number}\n\
        Account Type: {account.account_type}\n\
        Account Bank: {account.bank}\n\
        Account Opening: {account.open_date}\n\
        Account Balance : {account.deposit}\n\
        Credit Card : {account.credit_card}\n\
        Debit Card : {account.debit_card}"
        outfile = open('newaccounts.txt','w+')
        outfile.write(data)
        os.rename('newaccounts.txt', Account_file)
        outfile.close()

        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)

        # Define the full file path
        filepath = BASE_DIR + '/' + Account_file
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % Account_file
        return response




#-------------------------------------------------Transaction views ---------------------------------------------

class TransactionAPIView(generics.CreateAPIView) :
    """
    Renders a form for depositing and withdrawing from account of currently logged in user
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/transactions.html'
    serializer_class = TransactionsSerializer

    def get(self, request) :
        account = get_object_or_404(Account,user_id=request.user.id)
        serializer = TransactionsSerializer()
        form=TransactionForm
        return Response({'serializer' : serializer,'form':form,"account" : account})

    def post(self, request):
        serializer = TransactionsSerializer(data=request.data)
        account = get_object_or_404(Account,user_id=request.user.id)
        if serializer.is_valid():
            transaction_type = serializer.validated_data.get('transaction_type')
            amount = serializer.validated_data.get('amount')
            if(transaction_type == 'WITHDRAW') :
                if(amount>account.deposit) :
                    return HttpResponse("Balance is low")
                else:
                    account.deposit=account.deposit-amount
                    account.save()
            elif(transaction_type == 'DEPOSIT') :
                account.deposit=account.deposit+amount
                print(account.deposit)
                account.save()
            serializer.save(account=account,balance=account.deposit)
            url = f'http://127.0.0.1:8000/api/accounts/'
            return HttpResponseRedirect(redirect_to=url)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class TransactionDownloadAPIView(generics.ListAPIView) :  
    """
    Creates a transaction detail file  for the current account of logged in user, in txt format
    which is downloadable
    """ 
    def get(self, request):
        account = get_object_or_404(Account,user_id=request.user.id)

        transaction_list = Transactions.objects.filter(account=account)


        Transaction_file = f"{account.client.name}_transactions.txt"
        file = pathlib.Path(Transaction_file)
        if file.exists ():
            os.remove(Transaction_file)  #delete if file already present create new file
        data = f"Transaction Detail\n-------------------------------------------\n\""
        outfile = open('newaccounts.txt','w+')
        for transaction in transaction_list :
            data= data + f"Account Number: {account.number}\
            Transaction Type: {transaction.transaction_type}\
            Transaction Amount: {transaction.amount}\
            Account balance : {transaction.balance}\
            Transaction Date: {transaction.transaction_date}\
            \n"
        outfile.write(data)
        os.rename('newaccounts.txt', Transaction_file)
        outfile.close()

        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)

        # Define the full file path
        filepath = BASE_DIR + '/' + Transaction_file
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % Transaction_file
        return response


#-------------------------------------------------Transfer views ---------------------------------------------

class TransferAPIView(generics.CreateAPIView) :
    """
    Renders a form for transferring money from account of currently logged in user
    to another user stored in database
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "api/transfer.html"
    serializer_class = TransferSerializer

    def get(self, request) :
        serializer = TransferSerializer()
        form = TransferForm
        return Response({'serializer' : serializer,'form' : form})

    def post(self,request,*args,**kwargs):
        serializer1 = TransferSerializer(data=request.data)
        if serializer1.is_valid() :
            amount =serializer1.validated_data.get('amount')
            to_account = serializer1.validated_data.get('to_account')
            sender = get_object_or_404(Account,user_id=request.user.id)
        if sender.deposit > amount:
            # debit the sender account
                sender.deposit -= amount
                sender.save()
            #credit the receiver account
                receiver = Account.objects.get(number=to_account)
                receiver.deposit += amount
                receiver.save()
                serializer1.save(account=sender,from_balance=sender.deposit,to_balance=receiver.deposit)
        else :
            return HttpResponse("Balance is low")
        url = f"http://127.0.0.1:8000/api/accounts/"
        return HttpResponseRedirect(redirect_to=url)


class TransferDownloadAPIView(generics.ListAPIView) :   
    """
    Creates a transaction detail file  for the current account of logged in user, in txt format
    which is downloadable
    """ 
    def get(self, request,*args,**kwargs):
        account = get_object_or_404(Account,user_id=request.user.id)

        transfer_list = Transfer.objects.filter(account=account)
        print(transfer_list)


        Transfer_file = f"{account.client.name}_transfers.txt"
        file = pathlib.Path(Transfer_file)
        if file.exists ():
            os.remove(Transfer_file)  #delete if file already present create new file
        data = f"Transfer Detail Withdraw\n-------------------------------------------\n\""
        outfile = open('newaccounts.txt','w+')
        for transfer in transfer_list :
            data= data + f"Account Number: {transfer.to_account}\
            Transaction Amount: {transfer.amount}\
            Account balance : {transfer.from_balance}\
            Transfer Date : {transfer.transfer_date}\
            \n"
        outfile.write(data)
        data = f"Transfer Detail Deposit\n-------------------------------------------\n\""
        outfile.write(data)

        transfer_list = Transfer.objects.filter(to_account=account.number)
        print(transfer_list)
        for transfer in transfer_list :
            data= data + f"Account Number: {transfer.to_balance}\
            Transaction Amount: {transfer.amount}\
            Account balance : {transfer.balance}\
            Transfer Date : {transfer.transfer_date}\
            \n"
        outfile.write(data)

        os.rename('newaccounts.txt', Transfer_file)
        outfile.close()

        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)

        # Define the full file path
        filepath = BASE_DIR + '/' + Transfer_file
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % Transfer_file
        return response
