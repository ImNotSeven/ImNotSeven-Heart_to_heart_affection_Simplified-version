from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms

class registry(UserCreationForm):
    name = forms.CharField(required=True, max_length=15)
    nickname = forms.CharField(required=True, max_length=15)
    phone = forms.CharField(required=True, max_length=11)

    class Meta:
        model=User
        fields=('username','password1','password2','name','nickname','phone')

class edit(UserChangeForm):
    name = forms.CharField(required=True, max_length=15)
    nickname = forms.CharField(required=True, max_length=15)
    phone = forms.CharField(required=True, max_length=11)

    class Meta:
        model=User
        fields=('username','password','name','nickname','phone')