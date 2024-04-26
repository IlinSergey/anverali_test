from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContractorRegistrationForm, CustomerRegistrationForm


@login_required
def view_index(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/index.html')


class SignedOutView(TemplateView):
    template_name = 'registration/logged_out.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return render(request, self.template_name)


def register_customer(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = CustomerRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})


def register_contractor(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = ContractorRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = ContractorRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})
