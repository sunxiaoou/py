from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from app.models import UserToken


class Authentication(BaseAuthentication):
    def authenticate(self, request: Request):
        # token = request.GET.get('token')
        token = request.headers['Token']
        user_token = UserToken.objects.filter(token=token).first()
        if user_token:
            return user_token.user, token
        raise AuthenticationFailed('认证失败')
