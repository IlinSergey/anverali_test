from django.contrib import admin

from users.models import Contractor, Customer, Order, Response


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name',
                    'last_name', 'email', 'phone_number')
    list_filter = ('created_at',)
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name',
                    'email', 'phone_number', 'exprience')
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
