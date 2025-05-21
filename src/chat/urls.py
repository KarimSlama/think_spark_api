
from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('conversations/', views.get_user_conversations, name='user_conversations'),
    
]