from django import forms

from .models import Contractor, Customer, Order


class ContractorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = Contractor
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'password', 'password2', 'exprience')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = Customer
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'description')
