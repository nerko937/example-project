from rest_framework import serializers

from .models import Project, Issue, Attachment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'owner', 'creation_date', 'users')
        model = Project


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        fields = ('title', 'description', 'project', 'created_date', 'due_date', 'owner', 'assignee', 'status')
        read_only_fields = ('owner', 'created_date')
        model = Issue


class AttachmentSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Issue.objects.all())
    name = serializers.ReadOnlyField(source='file.name')
    size = serializers.ReadOnlyField(source='file.size')

    def validate_issue(self, val):
        user = self.context['request'].user
        if not (user == val.owner or user == val.assignee):
            raise serializers.ValidationError('You are not owner or assignee of this issue.')
        return val

    class Meta:
        fields = ('id', 'issue', 'file', 'name', 'size', 'created_date')
        read_only_fields = ('created_date',)
        model = Attachment
