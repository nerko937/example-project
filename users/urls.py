from allauth.socialaccount.providers.github.views import oauth2_login as github_oauth2_login
from allauth.socialaccount.providers.google.views import oauth2_login as google_oauth2_login
from django.urls import path


from .views import (
    UserListCreate,
    activate,
    GoogleLogin,
    google_callback,
    GithubLogin,
    github_callback,
)


urlpatterns = [
    # registration
    path('users/', UserListCreate.as_view(), name='users'),
    path('users/activate/<uuid:activation_id>/', activate, name='activate'),
    # google
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/url/', google_oauth2_login, name='google_url'),
    # github
    path('github/login/', GithubLogin.as_view(), name='github_login'),
    path('github/callback/', github_callback, name='github_callback'),
    path('github/url/', github_oauth2_login, name='github_url'),
]
