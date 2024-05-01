from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.SignedOutView.as_view(), name='logout'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('register_contractor/', views.register_contractor, name='register_contractor'),
    path('customer_personal_cabinet/', views.CustomerPersonalCabinetView.as_view(), name='customer_personal_cabinet'),
    path('contractor_personal_cabinet/',
         views.ContractorPersonalCabinetView.as_view(), name='contractor_personal_cabinet'),
]
