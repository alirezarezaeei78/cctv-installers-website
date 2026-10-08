"""
Serializers for the CCTV marketplace API.

These classes convert model instances to and from JSON representations
under Django REST Framework. They provide field validation and shape the
API responses consumed by the React front‑end.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from .models import Profile, ServiceRequest, Quote, RequestAttachment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default=Profile.ROLE_CUSTOMER)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    business_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone', 'business_name', 'address', 'bio']

    def validate(self, attrs):
        user = User(username=attrs['username'], email=attrs.get('email', ''))
        try:
            validate_password(attrs['password'], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'password': error.messages}) from error
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profile_data = {key: validated_data.pop(key) for key in
                        ('role', 'phone', 'business_name', 'address', 'bio') if key in validated_data}
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'phone', 'business_name', 'address', 'bio', 'verification_level']
        read_only_fields = ['verification_level']


class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    attachments = serializers.SerializerMethodField(read_only=True)
    # Accept a list of uploaded files when creating a request. The name
    # ``uploaded_files`` is chosen to avoid conflict with the read‑only
    # ``attachments`` field. Each element will be an instance of
    # ``django.core.files.uploadedfile.UploadedFile`` extracted from
    # ``request.FILES``.
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'customer',
            'title',
            'description',
            'buyer_type',
            'property_type',
            'address',
            'preferred_date',
            'preferred_time',
            'urgency',
            'created_at',
            'status',
            'attachments',
            'uploaded_files',
        ]
        read_only_fields = ['status']

    def get_attachments(self, obj):
        # Serialize attachment metadata (URL and upload time) for the API
        return [
            {
                'id': att.id,
                'file': att.file.url if att.file else '',
                'uploaded_at': att.uploaded_at,
            }
            for att in obj.attachments.all()
        ]

    @transaction.atomic
    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        service_request = ServiceRequest.objects.create(**validated_data)
        # Create attachment records for each uploaded file.
        for file in uploaded_files:
            RequestAttachment.objects.create(request=service_request, file=file)
        return service_request


class QuoteSerializer(serializers.ModelSerializer):
    installer = UserSerializer(read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'request', 'installer', 'message', 'price', 'created_at', 'accepted']
        read_only_fields = ['accepted']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value

    def validate_request(self, value):
        if value.status != 'open':
            raise serializers.ValidationError('This service request is closed.')
        return value
