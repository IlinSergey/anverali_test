import pytest
from pytest_django.asserts import assertTemplateUsed

from users.models import Customer


@pytest.mark.django_db
class TestCustomerPersonalCabinetView:
    def test__customer_personal_cabinet_view__success(self, client):
        client.force_login(Customer.objects.get(username='testcustomer'))
        response = client.get('/users/customer_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/customer_personal_cabinet.html')
        assert response.context['orders'].count() == 2

    def test__customer_personal_cabinet_view__not_customer(self, client, contractor_user):
        client.force_login(contractor_user)
        response = client.get('/users/customer_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/not_allowed.html')

    def test__customer_personal_cabinet_view__not_logged(self, client):
        response = client.get('/users/customer_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/not_allowed.html')
