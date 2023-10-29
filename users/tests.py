import jwt

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status

from ess.settings import SECRET_KEY
from rest_framework.test import APIClient


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_is_administrator_field(self):
        self.assertTrue(self.user.is_administrator)

    def test_generate_jwt_token(self):
        token = self.user._generate_jwt_token()
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = str(self.user.pk)
        self.assertEqual(payload['id'], user_id)
        expiration_time = timezone.make_aware(timezone.datetime.fromtimestamp(payload['exp']))
        expected_expiration_time = timezone.now() + timezone.timedelta(days=3)
        self.assertTrue(expiration_time > timezone.now())
        self.assertTrue(expiration_time < expected_expiration_time)

    def test_token_property(self):
        token = self.user.token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = str(self.user.pk)
        self.assertEqual(payload['id'], user_id)
        expiration_time = timezone.make_aware(timezone.datetime.fromtimestamp(payload['exp']))
        expected_expiration_time = timezone.now() + timezone.timedelta(days=3)
        self.assertTrue(expiration_time > timezone.now())
        self.assertTrue(expiration_time < expected_expiration_time)


class CreateUserAsAdminViewTest(TestCase):
    url = "http://127.0.0.1:8000/api/v1/create_user_as_admin"

    def setUp(self):
        self.client = APIClient()
        # Create an admin user (or mock it as needed)
        self.admin_user = get_user_model().objects.create(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_administrator=True
        )

    def test_create_user_as_admin_success(self):
        # Authenticate as the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Define user data for creating a new user
        user_data = {
                'email': 'newuser@example.com',
                'password': 'newuserpassword'
        }

        # Make a POST request to create a new user
        response = self.client.post(self.url, user_data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a new user was created
        self.assertTrue(get_user_model().objects.filter(email='newuser@example.com').exists())

    def test_create_user_as_admin_unauthenticated(self):
        # Make a POST request without authenticating as an admin
        user_data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'newuserpassword'
        }
        response = self.client.post(self.url, user_data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_admin_invalid_data(self):
        # Authenticate as the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Define invalid user data for creating a new user (e.g., missing required fields)
        invalid_user_data = {
                'username': 'invaliduser'
                # Missing 'email' and 'password' fields
        }

        # Make a POST request to create a new user with invalid data
        response = self.client.post(self.url, invalid_user_data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
