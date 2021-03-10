from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        User = get_user_model()
        u = User()
        u.is_active = True
        return u
