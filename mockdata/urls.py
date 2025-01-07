from django.urls import path
from . import views

urlpatterns = [
    path('api/mockdata/', views.send_mock_data),
]