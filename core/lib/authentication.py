"""
    This class extends RestFramework's original JWTAuthentication.
    We introduce check for HTTMLOnly cookies carrying access_toeken and refresh_token
"""
from typing import Optional, TypeVar
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import authentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import get_md5_hash_password
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.models import TokenUser

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Extract the token from the 'access_token' cookie
        rawToken = request.COOKIES.get('access_token')

        if rawToken is None:
            return None

        # Validate the token and return the user
        try:
            validatedToken = self.get_validated_token(rawToken)
            user = self.get_user(validatedToken)
            return (user, validatedToken)
        except Exception as e:
            # Handle token validation errors (e.g., expired token)
            return None

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Attempts to find and return a user using the given validated token.
        We should overwite this method, so we don't touch the Database instead
        storing all additional data in token's body.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as e:
            raise InvalidToken(
                _("Token contained no recognizable user identification")
            ) from e

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as e:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found"
            ) from e

        if api_settings.CHECK_USER_IS_ACTIVE and not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(user.password):
                raise AuthenticationFailed(
                    _("The user's password has been changed."), code="password_changed"
                )

        return user
