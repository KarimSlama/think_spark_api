from django.urls import path
from meetings import views

app_name = 'meetings'

urlpatterns = [
    path('schedule-meeting', views.schedule_meeting, name='schedule-meeting'),
    path('my-meetings/', views.my_scheduled_meetings, name='my-meetings'), 
    path('save_device_token/', views.save_device_token, name='save_device_token'), 
]
