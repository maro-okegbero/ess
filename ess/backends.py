"""
backends.py

@Author:    Maro Okegbero
@Date:      Oct @8, 2023


A simple jwt authentication handler
"""


import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication.

        """
        request.user = None

        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT
        # that it should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. No credentials provided or no Token prefix. Do not attempt to
            # authenticate. This is early exit
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate. This is early exit
            return None

        # This JWT library  can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # I simply have to decode `prefix` and `token` because I would get an error
        # if I didn't decode these values.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            return None

        # By now, we have satisfied the base requirement
        # We can now delegate the actual credentials authentication to the
        # method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the app and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

        except jwt.exceptions.ExpiredSignatureError:
            msg = 'Expired token, obtain a fresh token.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.exceptions.InvalidTokenError:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Wrong token. No app matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This app has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
