from django import forms

from .models import Contractor, Customer, Order, Response


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
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ('title', 'description')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        user = self.request.user
        if Order.objects.filter(title=title, customer=user).exists():
            raise forms.ValidationError('Заказ с таким названием уже существует.')
        return cleaned_data


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'description', 'is_active')


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
