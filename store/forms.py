from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import Account
from staff.models import Staff


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email')
    fname = forms.CharField(label='fname')
    lname = forms.CharField(label='lname')
    birthday = forms.DateField(label='birthday')
    gender = forms.IntegerField(label='gender')
    phone = forms.CharField(label='phone')
    address = forms.CharField(label='address')

    class Meta:
        model = Account
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("Email đã được sử dụng")

    def save(self, commit=True):
        Account.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['username'])
        user = Staff(fname=self.fname, lname=self.lname, account=Account.objects.get(username=self.cleaned_data['username']),
                     birthday=self.birthday, gender=self.gender, phone=self.phone, address=self.address, position=0)
        user.save()
        return user
