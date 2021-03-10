import urllib.parse

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.request import Request


def send_activation_email(user: User, request: Request) -> None:
    url = reverse('activate', args=[user.activation_id], request=request)
    send_mail(
        'Activate your account at Example Project',
        f'Navigate to below link to activate your account\n{url}',
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        html_message=f'Click at <a href="{url}">this link</a> to activate your account.',
    )


def get_callback_redirect(request: Request, service_name: str) -> redirect:
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'{settings.FRONTEND_URL}auth/{service_name}?{params}')
