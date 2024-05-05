import pytest
from pytest_django.asserts import assertTemplateUsed

from users.models import Contractor


@pytest.mark.django_db
class TestContractorPersonalCabinetView:
    def test__contractor_personal_cabinet_view__success(self, client):
        client.force_login(Contractor.objects.get(username='test'))
        response = client.get('/users/contractor_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/contractor_personal_cabinet.html')
        assert response.context['responses'].count() == 1

    def test__contractor_personal_cabinet_view__not_contractor(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('/users/contractor_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/not_allowed.html')

    def test__contractor_personal_cabinet_view__not_logged(self, client):
        response = client.get('/users/contractor_personal_cabinet/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/not_allowed.html')
