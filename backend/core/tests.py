"""Regression tests use an isolated, automatically discarded test database."""
import tempfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient
from .models import Profile, ServiceRequest, Quote


class MarketplaceTests(APITestCase):
    def setUp(self):
        self.password = 'Test-only-Large-River-482!'
        self.customer = self.make_user('customer', Profile.ROLE_CUSTOMER)
        self.other = self.make_user('other', Profile.ROLE_CUSTOMER)
        self.installer = self.make_user('installer', Profile.ROLE_INSTALLER)
        self.job = ServiceRequest.objects.create(customer=self.customer, title='CCTV', description='Install')

    def make_user(self, username, role):
        user = User.objects.create_user(username=username, password=self.password)
        Profile.objects.create(user=user, role=role)
        return user

    def test_anonymous_writes_are_rejected_without_database_error(self):
        self.assertEqual(self.client.post('/api/requests/', {'title': 'Test', 'description': 'Test'}).status_code, 403)
        self.assertEqual(self.client.post('/api/quotes/create/', {}).status_code, 403)

    def test_customer_can_create_request_with_optional_date_and_attachment(self):
        self.client.force_authenticate(self.customer)
        with tempfile.TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            response = self.client.post('/api/requests/', {
                'title': 'CCTV', 'description': 'Install',
                'uploaded_files': [SimpleUploadedFile('plan.txt', b'test plan')],
                'status': 'closed',
            }, format='multipart')
            self.assertEqual(response.status_code, 201, response.data)
            created = ServiceRequest.objects.get(pk=response.data['id'])
            self.assertEqual(created.customer, self.customer)
            self.assertIsNone(created.preferred_date)
            self.assertEqual(created.status, 'open')
            self.assertEqual(created.attachments.count(), 1)

    def test_customers_cannot_read_other_customer_requests(self):
        self.client.force_authenticate(self.other)
        self.assertEqual(len(self.client.get('/api/requests/').data), 0)
        self.assertEqual(self.client.get(f'/api/requests/{self.job.pk}/').status_code, 404)

    def test_only_installers_can_quote_and_acceptance_is_read_only(self):
        payload = {'request': self.job.pk, 'price': '10.00', 'message': 'Quote', 'accepted': True}
        self.client.force_authenticate(self.customer)
        self.assertEqual(self.client.post('/api/quotes/create/', payload).status_code, 403)
        self.client.force_authenticate(self.installer)
        response = self.client.post('/api/quotes/create/', payload)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertFalse(response.data['accepted'])

    def test_invalid_quote_and_filter_return_validation_errors(self):
        self.client.force_authenticate(self.installer)
        payload = {'request': self.job.pk, 'price': '-1', 'message': 'Quote'}
        self.assertEqual(self.client.post('/api/quotes/create/', payload).status_code, 400)
        self.job.status = 'closed'
        self.job.save()
        payload['price'] = '10'
        self.assertEqual(self.client.post('/api/quotes/create/', payload).status_code, 400)
        self.assertEqual(self.client.get('/api/quotes/?request=invalid').status_code, 400)

    def test_quotes_visible_only_to_participants(self):
        Quote.objects.create(request=self.job, installer=self.installer, price=10, message='Quote')
        for user, expected in [(self.other, 0), (self.customer, 1), (self.installer, 1)]:
            self.client.force_authenticate(user)
            self.assertEqual(len(self.client.get('/api/quotes/').data), expected)

    def test_registration_validates_role_password_and_duplicates(self):
        payload = {'username': 'newcustomer', 'password': self.password, 'role': 'admin'}
        self.assertEqual(self.client.post('/api/register/', payload).status_code, 400)
        self.assertFalse(User.objects.filter(username='newcustomer').exists())
        payload['role'] = 'customer'
        payload['password'] = '123'
        self.assertEqual(self.client.post('/api/register/', payload).status_code, 400)
        payload['password'] = self.password
        self.assertEqual(self.client.post('/api/register/', payload).status_code, 201)
        self.assertEqual(self.client.post('/api/register/', payload).status_code, 400)

    def test_browser_login_and_post_require_current_csrf_token(self):
        browser = APIClient(enforce_csrf_checks=True)
        credentials = {'username': 'customer', 'password': self.password}
        self.assertEqual(browser.post('/api/login/', credentials).status_code, 403)
        token = browser.get('/api/csrf/').json()['csrfToken']
        self.assertEqual(browser.post('/api/login/', credentials, HTTP_X_CSRFTOKEN=token).status_code, 200)
        payload = {'title': 'CCTV', 'description': 'Install'}
        self.assertEqual(browser.post('/api/requests/', payload).status_code, 403)
        token = browser.get('/api/csrf/').json()['csrfToken']
        self.assertEqual(browser.post('/api/requests/', payload, HTTP_X_CSRFTOKEN=token).status_code, 201)
