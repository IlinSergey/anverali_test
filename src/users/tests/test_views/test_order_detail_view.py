import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestOrderDetailView:

    @pytest.mark.parametrize('order_slug', [
        'telegram-bot',
        'django-site'
        ])
    def test__order_detail_view__success(self, client, customer_user, order_slug):
        client.force_login(customer_user)
        response = client.get(f'/orders/{order_slug}/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main/order_detail.html')

    def test__order_detail_view__not_found(self, client, customer_user):
        client.force_login(customer_user)
        response = client.get('/orders/not-found/')
        assert response.status_code == 404

    def test__order_detail_view__not_logged(self, client):
        response = client.get('/orders/telegram-bot/')
        assert response.status_code == 302

    def test__order_detail_view__method_not_allowed(self, client, contractor_user):
        client.force_login(contractor_user)
        response = client.post('/orders/telegram-bot/')
        assert response.status_code == 405
