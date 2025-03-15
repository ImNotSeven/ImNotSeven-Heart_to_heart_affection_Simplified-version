from django.contrib.auth.models import User
from django.db import models

class user_extend(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(blank=False,null=False,max_length=15)
    nickname=models.CharField(blank=False,null=False,max_length=15)
    phone=models.CharField(blank=False,null=False,max_length=11)

    class Meta:
        verbose_name_plural="user_extend"

