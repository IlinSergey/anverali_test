import pytest
from pytest_django.asserts import assertTemplateUsed

from users.forms import OrderForm
from users.models import Customer, Order


@pytest.mark.django_db
class TestOrderCreateView:

    def test__order_create_view__success_get(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('/add_order/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/order_create.html')
        assert response.context['form'] is not None
        assert isinstance(response.context['form'], OrderForm)

    def test__order_create_view__success_post(self, client, customer_user):
        client.force_login(customer_user)
        form = OrderForm(data={
            'title': 'test_title',
            'description': 'test_description',
            })
        response = client.post('/add_order/', data=form.data)
        assert response.status_code == 200
        added_order = Order.objects.get(title='test_title')
        assert added_order is not None
        added_order.delete()

    def test__order_create_view__exist(self, client):
        client.force_login(Customer.objects.get(username='testcustomer'))
        form = OrderForm(data={
            'title': 'Telegram бот',
            'description': 'Написать телеграм бота для отслеживания курсов акций',
            })
        response = client.post('/add_order/', data=form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            '__all__': ['Заказ с таким названием уже существует.'],
        }

    def test__order_create_view__not_valid_form(self, client, customer_user):
        client.force_login(customer_user)
        form = OrderForm(data={})
        response = client.post('/add_order/', data=form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            'title': ['Обязательное поле.'],
            'description': ['Обязательное поле.'],
        }

    def test__order_create_view__not_customer(self, client, contractor_user):
        client.force_login(contractor_user)
        response = client.get('/add_order/')
        assert response.status_code == 200
        assert response.context.get('form') is None
        assertTemplateUsed(response, 'main/not_allowed_order.html')
