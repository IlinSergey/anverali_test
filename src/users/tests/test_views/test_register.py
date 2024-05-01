import pytest
from pytest_django.asserts import assertTemplateUsed

from users.models import Contractor, Customer


@pytest.mark.django_db
class TestRegisterContractorView:
    def test__register_contractor_view__succes_get(self, client):
        response = client.get('/users/register_contractor/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')

    def test__register_contractor_view__succes_post(self, client):
        response = client.post('/users/register_contractor/', {
            'username': 'test_contractor_user',
            'first_name': 'test_contractor_name',
            'email': 'test_contractor@test.com',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password',
            'exprience': 1
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register_done.html')
        created_user = Contractor.objects.get(username='test_contractor_user')
        assert created_user is not None
        assert created_user.check_password('test_password')
        assert created_user.exprience == 1
        assert created_user.first_name == 'test_contractor_name'
        created_user.delete()

    def test__register_contractor_view__user_exists(self, client, contractor_user):
        response = client.post('/users/register_contractor/', {
            'username': 'test_contractor_user',
            'first_name': 'test_contractor_name',
            'email': 'test_contractor@test.com',
            'phone_number': '123456788',
            'password': 'test_password',
            'password2': 'test_password',
            'exprience': 1
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'username': ['Пользователь с таким именем уже существует.'],
        }

    def test__register_contractor_view__different_password(self, client):
        response = client.post('/users/register_contractor/', {
            'username': 'test_contractor_user',
            'first_name': 'test_contractor_name',
            'email': 'test_contractor@test.com',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password2',
            'exprience': 1
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'password2': ['Пароли не совпадают'],
        }

    def test__register_contractor_view__invalid_email(self, client):
        response = client.post('/users/register_contractor/', {
            'username': 'test_contractor_user',
            'first_name': 'test_contractor_name',
            'email': 'test_contractor',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password',
            'exprience': 1
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'email': ['Введите правильный адрес электронной почты.'],
        }


@pytest.mark.django_db
class TestRegisterCustomerView:
    def test__register_customer_view__succes_get(self, client):
        response = client.get('/users/register_customer/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')

    def test__register_customer_view__succes_post(self, client):
        response = client.post('/users/register_customer/', {
            'username': 'test_customer_user',
            'first_name': 'test_customer_name',
            'email': 'test_customer@test.com',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password',
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register_done.html')
        created_user = Customer.objects.get(username='test_customer_user')
        assert created_user is not None
        assert created_user.check_password('test_password')
        assert created_user.first_name == 'test_customer_name'
        created_user.delete()

    def test__register_customer_view__user_exists(self, client, customer_user):
        response = client.post('/users/register_customer/', {
            'username': 'test_customer_user',
            'first_name': 'test_customer_name',
            'email': 'test_customer@test.com',
            'phone_number': '123456788',
            'password': 'test_password',
            'password2': 'test_password',
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'username': ['Пользователь с таким именем уже существует.'],
        }

    def test__register_customer_view__different_password(self, client):
        response = client.post('/users/register_customer/', {
            'username': 'test_customer_user',
            'first_name': 'test_customer_name',
            'email': 'test_customer@test.com',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password2',
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'password2': ['Пароли не совпадают'],
        }

    def test__register_customer_view__invalid_email(self, client):
        response = client.post('/users/register_customer/', {
            'username': 'test_customer_user',
            'first_name': 'test_customer_name',
            'email': 'test_customer',
            'phone_number': '123456789',
            'password': 'test_password',
            'password2': 'test_password',
        })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'email': ['Введите правильный адрес электронной почты.'],
        }
