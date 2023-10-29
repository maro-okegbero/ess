import jwt

from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models

from ess.base_model import BaseModelClass
from ess.settings import SECRET_KEY


class User(AbstractUser, BaseModelClass):
    """
    The user model
    """
    is_administrator = models.BooleanField(null=False, blank=False, default=True)

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this app's ID and has an expiry
        date set to 3 days into the future.
        """
        dt = datetime.now() + timedelta(days=3)

        token = jwt.encode({
                'id': str(self.pk),
                'exp': int(dt.strftime('%s'))
        }, SECRET_KEY, algorithm='HS256')
        return token

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `app.token` instead of
        `app.generate_jwt_token().
        """
        return self._generate_jwt_token()
