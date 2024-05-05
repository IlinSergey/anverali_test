import pytest
from pytest_django.asserts import assertTemplateUsed

from users.models import Response


@pytest.mark.django_db
class TestResponseAddView:
    def test__response_add_view__success_get(self, client, contractor_user):
        client.force_login(contractor_user)
        data = {
            'message': 'Тестовое сообщение',
        }
        response = client.post('/3/response/', data=data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/response_done.html')
        added_response = Response.objects.get(message='Тестовое сообщение')
        assert added_response is not None
        added_response.delete()

    def test__response_add_view__not_valid_form(self, client, contractor_user):
        client.force_login(contractor_user)
        data = {}
        response = client.post('/2/response/', data=data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/response.html')

    def test__response_add_view__not_contractor(self, client, customer_user):
        client.force_login(customer_user)
        data = {
            'message': 'Тестовое сообщение',
        }
        response = client.post('/3/response/', data=data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/not_allowed_response.html')

    def test__response_add_view__method_not_allowed(self, client, contractor_user):
        client.force_login(contractor_user)
        data = {
            'message': 'Тестовое сообщение',
        }
        response = client.put('/3/response/', data=data)
        assert response.status_code == 405
