from . import views
from django.urls import path

app_name = 'preferences'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('filters/', views.filter_list, name='filter_list'),
    path('locations/', views.location_list, name='location_list'),
    path('categories_related_ideas/', views.categories_with_ideas, name='categories_with_ideas'),
]