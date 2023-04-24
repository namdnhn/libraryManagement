from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import Account
from user.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("Email đã được sử dụng")

    def save(self, commit=True):
        Account.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        user = User(fname='Unknown', lname='', account=Account.objects.get(username=self.cleaned_data['username']))
        user.save()
