from rest_framework import serializers

from .models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Issue
