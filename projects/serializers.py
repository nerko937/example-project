from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'owner', 'creation_date', 'users')
        model = Project
