from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .permissions import CanCreateOrIsAuthenticated
from .serializers import UserSerializer
from .utils import send_activation_email, get_callback_redirect


class UserListCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (CanCreateOrIsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user, self.request)


@api_view(['GET'])
def activate(request, activation_id):
    activation_obj = get_object_or_404(get_user_model(), activation_id=activation_id)
    activation_obj.user.is_active = True
    activation_obj.user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('google_callback'))


def google_callback(request):
    return get_callback_redirect(request, 'google')


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('github_callback'))


def github_callback(request):
    return get_callback_redirect(request, 'github')


def account_inactive(request):
    return redirect(f'{settings.FRONTEND_URL}/user-inactive')
