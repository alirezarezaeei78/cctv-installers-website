"""
Django admin configuration for the core models.

Register models with customized list displays to improve the admin
experience. Admin pages allow staff to manage users, profiles, service
requests, and quotes through a graphical interface.
"""
from django.contrib import admin
from .models import Profile, ServiceRequest, Quote, RequestAttachment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'business_name', 'verification_level')
    list_filter = ('role', 'verification_level')
    search_fields = ('user__username', 'user__email', 'business_name', 'phone')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'customer',
        'buyer_type',
        'urgency',
        'status',
        'created_at',
    )
    list_filter = ('status', 'buyer_type', 'urgency')
    search_fields = (
        'title',
        'description',
        'customer__username',
        'address',
        'property_type',
    )


@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('request__title',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'installer', 'price', 'accepted', 'created_at')
    list_filter = ('accepted',)
    search_fields = ('request__title', 'installer__username')