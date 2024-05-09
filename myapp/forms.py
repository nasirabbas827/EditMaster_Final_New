from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class userform(UserCreationForm):
    father_name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'father_name', 'gender', 'address')


class userchangeform(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')



class userchangepassform(PasswordChangeForm):
    pass


from django import forms

class UploadPdfForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')
