from django.urls import path

from .views import UserRegisterView, activate


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('activate/<uuid:unique_id>/', activate, name='activate'),
]
