"""Session-authenticated marketplace endpoints."""
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from rest_framework import generics, views, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Profile, ServiceRequest, Quote
from .serializers import (
    UserSerializer, RegistrationSerializer, ProfileSerializer,
    ServiceRequestSerializer, QuoteSerializer,
)


@require_GET
def csrf_token(request):
    """Bootstrap the CSRF cookie before a browser submits a form."""
    return JsonResponse({'csrfToken': get_token(request)})


def require_role(user, role):
    if not Profile.objects.filter(user=user, role=role).exists():
        raise PermissionDenied('Your account cannot perform this action.')


@method_decorator(csrf_protect, name='dispatch')
class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            raise ValidationError({'username': 'This username is already registered.'})
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.data.get('username'),
                            password=request.data.get('password'))
        if user is None:
            return Response({'detail': 'نام کاربری یا گذرواژه اشتباه است.'},
                            status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'detail': 'ورود موفقیت آمیز بود.'})


class InstallerListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(role=Profile.ROLE_INSTALLER).select_related('user')


class ServiceRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        queryset = ServiceRequest.objects.select_related('customer').prefetch_related('attachments')
        if Profile.objects.filter(user=self.request.user, role=Profile.ROLE_INSTALLER).exists():
            return queryset
        return queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        require_role(self.request.user, Profile.ROLE_CUSTOMER)
        serializer.save(customer=self.request.user)


class ServiceRequestDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer
    get_queryset = ServiceRequestListCreateView.get_queryset


class QuoteCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuoteSerializer

    def perform_create(self, serializer):
        require_role(self.request.user, Profile.ROLE_INSTALLER)
        serializer.save(installer=self.request.user)


class QuoteListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuoteSerializer

    def get_queryset(self):
        queryset = Quote.objects.filter(
            Q(installer=self.request.user) | Q(request__customer=self.request.user)
        ).select_related('installer', 'request')
        request_id = self.request.query_params.get('request')
        if request_id:
            try:
                request_id = int(request_id)
                if request_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                raise ValidationError({'request': 'Expected a positive request ID.'})
            queryset = queryset.filter(request_id=request_id)
        return queryset
