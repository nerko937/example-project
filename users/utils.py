from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.request import Request


def send_activation_email(user: User, request: Request) -> None:
    url = reverse('activate', args=[user.activation.unique_id], request=request)
    send_mail(
        'Activate your account at Example Project',
        f'Navigate to below link to activate your account\n{url}',
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        html_message=f'Click at <a href="{url}">this link</a> to activate your account.',
    )
