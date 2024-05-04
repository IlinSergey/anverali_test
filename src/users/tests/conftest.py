import os

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from users.models import Contractor, Customer


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        ContentType.objects.all().delete()
        current_dir = os.path.dirname(__file__)
        initial_data_path = os.path.join(current_dir, 'initial_data.json')
        call_command('loaddata', initial_data_path, verbosity=0)
        yield


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
