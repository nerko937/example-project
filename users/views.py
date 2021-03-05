from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .utils import send_activation_email


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

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
