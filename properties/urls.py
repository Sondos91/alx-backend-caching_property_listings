from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('test-cache/', views.test_cache, name='test_cache'),
    path('list/', views.property_list, name='property_list'),
]
