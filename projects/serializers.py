from rest_framework import serializers

from .models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        fields = ('title', 'description', 'project', 'created_date', 'due_date', 'owner', 'assignee', 'status')
        read_only_fields = ('owner', 'created_date')
        model = Issue
