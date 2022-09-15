from django.urls import path

from .views import *

app_name = 'api'
urlpatterns = [
    path('',IndexView.as_view(),name = "index"),

    path('branches/',BranchesAPIView.as_view(), name="branches"),

    path('banks/',BanksAPIView.as_view(),name="banks"),

    path('accounts/',AccountUserListView.as_view(),name="accounts"), 
    path('create_account/',CreateAccountAPIView.as_view(),name="create-account"),
    path('update_account/',UpdateAccountAPIView.as_view(),name="update-account"),
    path('download_account/',DownloadAccountAPIView.as_view(),name='download-account'),

    path('update_client/',UpdateClientAPIView.as_view(),name="update-client"),
    path('client/',UserListView.as_view(),name="user"), 
    path('create_client/',CreateClientAPIView.as_view(),name='create-client'),
    path('download_client/',DownloadClientAPIView.as_view(),name='download-client'),

    path('transactions/',TransactionAPIView.as_view(),name='transaction'),
    path('download_transactions/',TransactionDownloadAPIView.as_view(),name='download-transaction'),
    path('transfers/',TransferAPIView.as_view(),name='transfer'),
    path('download_transfers/',TransferDownloadAPIView.as_view(),name='download-transfer'),
    
] 