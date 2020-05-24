from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Person, Office, Area, Request

class PersonField(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['birthdate', 'birthplace', 'account']
        labels = {
            'birthdate' : _('Daty nahaterahana'),
            'birthplace' : _('Toerana nahaterahana')
        }

class NewPersonField(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['birthdate', 'birthplace']
        labels = {
            'birthdate' : _('Daty nahaterahana'),
            'birthplace' : _('Toerana nahaterahana')
        }



class OfficeField(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['center']

class AreaField(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'center']

class RequestField(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['dup_number', 'requester', 'office']

class UserField(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'last_name', 'first_name']

        labels = {
            'last_name' : _('Anarana'),
            'first_name' : _('Fanampin\'anarana')
        }