import pytest
from pytest_django.asserts import assertTemplateUsed

from users.forms import OrderEditForm
from users.models import Customer, Order


@pytest.mark.django_db
class TestOrderEditView:

    def test__order_edit_view__success(self, client):
        client.force_login(Customer.objects.get(username='testcustomer'))
        response = client.get('/orders/testcustomer-telegram/edit/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/order_edit.html')
        assert response.context['form'].__class__.__name__ == 'OrderEditForm'
        assert response.context['order'].title == 'Telegram бот'
        updated_data = {
            'title': 'test_title',
            'description': response.context['order'].description,
        }
        form = OrderEditForm(data=updated_data)
        assert form.is_valid()
        response = client.post('/orders/testcustomer-telegram/edit/', data=form.data)
        updated_order = Order.objects.get(title='test_title')
        assert updated_order is not None
        updated_order.title = 'Telegram бот'
        updated_order.save()

    def test__order_edit_view__not_valid_form(self, client):
        client.force_login(Customer.objects.get(username='testcustomer'))
        form = OrderEditForm(data={})
        response = client.post('/orders/testcustomer-telegram/edit/', data=form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            'title': ['Обязательное поле.'],
            'description': ['Обязательное поле.'],
        }

    def test__order_edit_view__not_customer(self, client, contractor_user):
        client.force_login(contractor_user)
        response = client.get('/orders/testcustomer-telegram/edit/')
        assert response.status_code == 200
        assert response.context.get('form') is None
        assertTemplateUsed(response, 'main/not_allowed.html')

    def test__order_edit_view__not_found(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('/orders/not-found/edit/')
        assert response.status_code == 404

    def test__order_edit_view__method_not_allowed(self, client, customer_user):
        client.force_login(customer_user)
        response = client.delete('/orders/testcustomer-telegram/edit/')
        assert response.status_code == 405
