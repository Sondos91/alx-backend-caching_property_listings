from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('test-cache/', views.test_cache, name='test_cache'),
]
