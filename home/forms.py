from django import forms
import re
from home.models import Account


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', error_messages={'required': 'Quay lại điền username đê'})
    email = forms.EmailField(label='Email', error_messages={'required': 'Quay lại điền email đê'})
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(),
                                error_messages={'required': 'Quay lại điền password đê'})
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput(),
                                error_messages={'required': 'Quay lại điền xác nhận password đê'})

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            Account.objects.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("Email đã được sử dụng")

    def save(self):
        Account.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
