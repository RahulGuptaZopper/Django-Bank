from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Branch)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Client)