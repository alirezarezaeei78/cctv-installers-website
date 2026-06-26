"""
Serializers for the CCTV marketplace API.

These classes convert model instances to and from JSON representations
under Django REST Framework. They provide field validation and shape the
API responses consumed by the React front‑end.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ServiceRequest, Quote, RequestAttachment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'phone', 'business_name', 'address', 'bio', 'verification_level']


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

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None
        service_request = ServiceRequest.objects.create(customer=user, **validated_data)
        # Create attachment records for each uploaded file.
        for file in uploaded_files:
            RequestAttachment.objects.create(request=service_request, file=file)
        return service_request


class QuoteSerializer(serializers.ModelSerializer):
    installer = UserSerializer(read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'request', 'installer', 'message', 'price', 'created_at', 'accepted']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None
        return Quote.objects.create(installer=user, **validated_data)