from django.contrib.auth.models import AbstractUser
from django.db import models

class CmmsUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username
