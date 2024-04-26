from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.SignedOutView.as_view(), name='logout'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('register_contractor/', views.register_contractor, name='register_contractor'),

    path('index/', views.view_index, name='index'),
]
