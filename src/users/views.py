from typing import Any

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from .forms import (ContractorRegistrationForm, CustomerRegistrationForm,
                    OrderEditForm, OrderForm, ResponseForm)
from .models import Order, Response


class IndexView(LoginRequiredMixin, View):
    template_name = 'main/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        orders_list = Order.active.all()
        paginator = Paginator(orders_list, 10)
        page_number = request.GET.get('page', 1)
        try:
            orders = paginator.get_page(page_number)
        except PageNotAnInteger:
            orders = paginator.get_page(1)
        except EmptyPage:
            orders = paginator.get_page(paginator.num_pages)
        return render(request, self.template_name, {'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'main/order_detail.html'

    def get(self, request: HttpRequest, order_slug: str) -> HttpResponse:
        order = get_object_or_404(Order.objects.select_related('customer'), slug=order_slug)
        responses = order.responses.all().select_related('contractor').order_by('-created_at')
        user_responsed = False
        is_contractor = hasattr(request.user, 'contractor')
        if request.user.is_authenticated and is_contractor:
            user_responsed = responses.filter(contractor=request.user.contractor).exists()
        form = ResponseForm()
        return render(request, self.template_name, {'order': order, 'responses': responses,
                                                    'form': form, 'user_responsed': user_responsed,
                                                    'is_contractor': is_contractor})


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


class OrderCreateView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'main/order_create.html'
    redirect_template_name = 'main/order_done.html'
    not_allowed_template_name = 'main/not_allowed_order.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not hasattr(request.user, 'customer'):
            return render(request, self.not_allowed_template_name)
        return super().dispatch(request, *args, **kwargs)

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


class OrderEditView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderEditForm
    template_name = 'main/order_edit.html'
    success_url = 'order_detail'
    not_allowed_template_name = 'main/not_allowed.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not hasattr(request.user, 'customer'):
            return render(request, self.not_allowed_template_name)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'order_slug': self.object.slug})

    def get_object(self, queryset=None):
        return get_object_or_404(Order, slug=self.kwargs['order_slug'])


class ResponseAddView(View):
    login_url = 'users:login'
    template_name = ''
    redirect_template_name = 'main/response_done.html'
    not_allowed_template_name = 'main/not_allowed_response.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not hasattr(request.user, 'contractor'):
            return render(request, self.not_allowed_template_name)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, order_id: int) -> HttpResponse:
        if hasattr(request.user, 'contractor'):
            order = get_object_or_404(Order, id=order_id)
            response = None
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.order = order
                response.contractor = request.user.contractor
                response.save()
                return render(request, self.redirect_template_name, {'response': response})
            return render(request, self.template_name, {'response_form': response_form,
                                                        'order': order})
        return render(request, self.not_allowed_template_name)


class CustomerPersonalCabinetView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/customer_personal_cabinet.html'
    not_allowed_template_name = 'main/not_allowed.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not hasattr(request.user, 'customer'):
            return render(request, self.not_allowed_template_name)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        orders = Order.objects.select_related('customer').filter(customer=request.user)
        return render(request, self.template_name, {'orders': orders})


class ContractorPersonalCabinetView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/contractor_personal_cabinet.html'
    not_allowed_template_name = 'main/not_allowed.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not hasattr(request.user, 'contractor'):
            return render(request, self.not_allowed_template_name)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        responses = Response.objects.filter(contractor=request.user)
        return render(request, self.template_name, {'responses': responses})
