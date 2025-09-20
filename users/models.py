from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField('is admin',default=False)
    is_user = models.BooleanField('is user',default=False)
    is_doctor = models.BooleanField('is doctor',default=False)
