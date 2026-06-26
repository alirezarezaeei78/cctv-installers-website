"""
Views for the CCTV marketplace API.

This module defines API endpoints using Django REST Framework. It
provides basic functionality for registering users, listing installers,
posting service requests, and submitting quotes. Authentication is
implemented via the Django session backend for simplicity. This code can
be extended to add token authentication or permission checks as needed.
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, views, status
from rest_framework.response import Response

from .models import Profile, ServiceRequest, Quote
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ServiceRequestSerializer,
    QuoteSerializer,
)


class RegisterView(views.APIView):
    """Register a new user and associated profile."""

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        role = request.data.get('role', Profile.ROLE_CUSTOMER)
        phone = request.data.get('phone', '')
        business_name = request.data.get('business_name', '')
        address = request.data.get('address', '')
        bio = request.data.get('bio', '')
        if not username or not password:
            return Response({'detail': 'نام کاربری و گذرواژه الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'این نام کاربری قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            business_name=business_name,
            address=address,
            bio=bio,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    """Authenticate a user and create a session."""

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'نام کاربری یا گذرواژه اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'detail': 'ورود موفقیت آمیز بود.'}, status=status.HTTP_200_OK)


class InstallerListView(generics.ListAPIView):
    """List all installer profiles."""
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(role=Profile.ROLE_INSTALLER)


class ServiceRequestListCreateView(generics.ListCreateAPIView):
    """List existing service requests or create a new request."""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def perform_create(self, serializer):
        serializer.save()


class ServiceRequestDetailView(generics.RetrieveAPIView):
    """Retrieve a single service request and its quotes."""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer


class QuoteCreateView(generics.CreateAPIView):
    """Create a quote for a specific service request."""
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteListView(generics.ListAPIView):
    """List all quotes for a given service request via query param ``request``."""
    serializer_class = QuoteSerializer

    def get_queryset(self):
        request_id = self.request.query_params.get('request')
        qs = Quote.objects.all()
        if request_id:
            qs = qs.filter(request_id=request_id)
        return qs