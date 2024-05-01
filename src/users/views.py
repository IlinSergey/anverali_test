from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from .forms import (ContractorRegistrationForm, CustomerRegistrationForm,
                    OrderForm)
from .models import Order


@login_required
def view_index(request: HttpRequest) -> HttpResponse:
    orders = Order.active.all()
    return render(request, 'main/index.html', {'orders': orders})


class IndexView(LoginRequiredMixin, View):
    template_name = 'main/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        orders = Order.active.all()
        return render(request, self.template_name, {'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'main/order_detail.html'

    def get(self, request: HttpRequest, order_id: int) -> HttpResponse:
        order = get_object_or_404(Order.active.select_related('customer'), id=order_id)
        return render(request, self.template_name, {'order': order})


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


class OrderCreate(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'main/order_create.html'
    redirect_template_name = 'main/order_done.html'
    not_allowed_template_name = 'main/not_allowed.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        order_form = OrderForm()
        return render(request, self.template_name, {'order_form': order_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        if hasattr(request.user, 'customer'):
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                new_order = order_form.save(commit=False)
                new_order.customer = request.user.customer
                new_order.save()
                return render(request, self.redirect_template_name, {'new_order': new_order})
            return render(request, self.template_name, {'order_form': order_form})
        return render(request, self.not_allowed_template_name)
