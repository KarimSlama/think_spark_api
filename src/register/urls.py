from . import views
from django.urls import path

app_name = 'register'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('request_password_rest/', views.request_password_rest, name='request_password_rest'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('reset_password/', views.reset_password, name='reset_password'),
]