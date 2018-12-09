from django import forms
from .models import Testimony
from django.contrib.auth.models import User


class TestimonyForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=False)
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    to_name = forms.CharField(max_length=30, required=False)
    commented = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #profile_pic = forms.ImageField()
    class Meta:
        model = Testimony
        fields = ('name', 'to_name','commented')
