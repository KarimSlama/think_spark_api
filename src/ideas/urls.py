from . import views
from django.urls import path

app_name = 'ideas'

urlpatterns = [
    path('', views.idea_list_upload, name='idea_list_upload'),
    path('idea_details/<int:id>', views.idea_details , name='idea_details'),

]