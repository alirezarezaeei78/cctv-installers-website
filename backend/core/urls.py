"""
URL routes for the CCTV marketplace API.

These routes expose endpoints for user registration, authentication,
installer discovery, service request management, and quoting. Prefix
this URLconf under ``/api/`` in the project’s main URL configuration.
"""
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('installers/', views.InstallerListView.as_view(), name='installer-list'),
    path('requests/', views.ServiceRequestListCreateView.as_view(), name='service-request-list'),
    path('requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service-request-detail'),
    path('quotes/', views.QuoteListView.as_view(), name='quote-list'),
    path('quotes/create/', views.QuoteCreateView.as_view(), name='quote-create'),
]