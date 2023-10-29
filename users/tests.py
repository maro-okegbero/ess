from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import jwt
from ess.settings import SECRET_KEY


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
