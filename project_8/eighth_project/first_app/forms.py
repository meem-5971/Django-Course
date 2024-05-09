from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

class ChangeUserData(UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']