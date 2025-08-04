from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.connection_status),
]
