from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Activation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short (min. 8 characters).")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'].split('@')[0],
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()
        a = Activation.objects.create(user=user)
        print(a.unique_id)
        return user

    class Meta:
        model = User
        fields = ('email', 'password')
