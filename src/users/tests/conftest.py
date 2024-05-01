import pytest

from users.models import Contractor, Customer


@pytest.fixture
def contractor_user():
    contractor = Contractor.objects.create_user(
        username='test_contractor_user',
        first_name='test_contractor_name',
        email='test_contractor@test.com',
        phone_number='123456789',
        password='test_password',
        exprience=1
    )
    yield contractor
    contractor.delete()


@pytest.fixture
def customer_user():
    customer = Customer.objects.create_user(
        username='test_customer_user',
        first_name='test_customer_name',
        email='test_customer@test.com',
        phone_number='123456789',
        password='test_password'
    )
    yield customer
    customer.delete()
