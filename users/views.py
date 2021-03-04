from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Activation
from .serializers import UserSerializer
from .utils import send_activation_email


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user, self.request)


@api_view(['GET'])
def activate(request, unique_id):
    activation_obj = get_object_or_404(Activation, unique_id=unique_id)
    activation_obj.user.is_active = True
    activation_obj.user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
