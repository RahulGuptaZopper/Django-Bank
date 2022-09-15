from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='User_name',max_length=20,unique=True)
    email = models.EmailField(db_index=True, unique=True,)
    
    # add additional fields in here

    def __str__(self):
        return self.username