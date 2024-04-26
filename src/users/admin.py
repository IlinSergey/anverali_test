from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import Contractor, Customer, Order, Response


admin.site.unregister(Group)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ('username', 'password', 'first_name',
                    'last_name', 'email', 'phone_number', 'is_customer')
    list_filter = ('created_at',)
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Contractor)
class ContractorAdmin(UserAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name',
                    'email', 'phone_number', 'exprience', 'is_contractor')
    list_filter = ('created_at',)
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'customer', 'is_active')
    list_filter = ('is_active', 'created_at', 'customer')
    search_fields = ('title',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('order', 'contractor', 'message')
    list_filter = ('created_at', 'order', 'contractor')
    search_fields = ('message',)
