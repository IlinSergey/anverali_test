import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestIndexView:

    def test__index_view__not_logged(self, client):
        response = client.get('')
        assert response.status_code == 302

    def test__index_view__logged_as_customer(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/index.html')

    def test__index_view__logged_as_contractor(self, client, contractor_user):
        client.force_login(contractor_user)
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/index.html')

    def test__index_view__logged_check_data(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/index.html')
        assert response.context['page_obj'].paginator.num_pages == 1
        assert len(response.context['orders'].paginator.object_list) == 2
