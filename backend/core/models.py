"""
Database models for the CCTV marketplace.

These models provide a simplified representation of users, installers,
service requests, and quotes. They are designed to support a two‑sided
marketplace in which customers can post installation requests and
installers can respond with quotes. The fields here are minimal to keep
the MVP manageable but can be extended easily.
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extend the built‑in User model with marketplace‑specific fields."""
    ROLE_CUSTOMER = 'customer'
    ROLE_INSTALLER = 'installer'
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_INSTALLER, 'Installer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    business_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    verification_level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"


class ServiceRequest(models.Model):
    """A request posted by a customer for CCTV installation services.

    In addition to a simple title and description, this model captures
    structured data needed to match installers effectively. Customers
    identify their buyer persona (homeowner, business owner, or property
    manager), specify the property type and address, indicate a preferred
    installation date/time window, and convey the urgency of the job. A
    rich description field allows for free‑form details. The request can
    have multiple attachments such as photos or floor plans uploaded via
    the related ``RequestAttachment`` model.
    """

    # Buyer personas reflect the key customer segments described in the
    # blueprint: homeowners, small business owners, and property managers.
    BUYER_HOME = 'home'
    BUYER_BUSINESS = 'business'
    BUYER_MANAGER = 'manager'
    BUYER_CHOICES = [
        (BUYER_HOME, 'Home'),
        (BUYER_BUSINESS, 'Business'),
        (BUYER_MANAGER, 'Property Manager'),
    ]

    # Urgency levels help installers prioritize incoming work. Use simple
    # wording rather than numeric values to aid UX translation.
    URGENCY_LOW = 'low'
    URGENCY_MEDIUM = 'medium'
    URGENCY_HIGH = 'high'
    URGENCY_CHOICES = [
        (URGENCY_LOW, 'Low'),
        (URGENCY_MEDIUM, 'Medium'),
        (URGENCY_HIGH, 'High'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    buyer_type = models.CharField(max_length=10, choices=BUYER_CHOICES, default=BUYER_HOME)
    property_type = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=20, blank=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default=URGENCY_MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='open')

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.title} by {self.customer.username}"


class RequestAttachment(models.Model):
    """File attachments associated with a service request.

    Customers can upload photos or floor plans to provide installers with
    better context about the installation site. Files are stored in the
    ``request_attachments/`` directory under ``MEDIA_ROOT``. The
    ``uploaded_at`` timestamp facilitates ordering and audit trails.
    """

    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='request_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Request Attachment'
        verbose_name_plural = 'Request Attachments'
        ordering = ['uploaded_at']

    def __str__(self) -> str:
        return f"Attachment {self.id} for request {self.request_id}"


class Quote(models.Model):
    """A quote provided by an installer in response to a service request."""
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='quotes')
    installer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    message = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Quote'
        verbose_name_plural = 'Quotes'
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"Quote {self.id} for request {self.request.id} by {self.installer.username}"