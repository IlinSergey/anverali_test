from django.contrib.auth.backends import ModelBackend

from .models import Contractor, Customer


class CustomerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user


class ContractorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Contractor.objects.get(username=username)
        except Contractor.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
