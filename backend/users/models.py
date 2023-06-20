from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

    profilePic = models.CharField(max_length=100, default='https://api.multiavatar.com/a.svg')
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return '{}'.format(self.email)
    