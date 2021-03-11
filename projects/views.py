from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .models import Project, Issue, Attachment
from .permissions import IsOwnerOrReadOnly, IsIssueOwner
from .serializers import ProjectSerializer, IssueSerializer, AttachmentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ('head', 'get', 'post', 'put', 'patch')

    def get_queryset(self):
        return Project.objects.filter(Q(users=self.request.user) | Q(owner=self.request.user))


class IssueCreate(generics.CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)


class IssueRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class IssueListForProject(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_id'])


class AttachmentCreate(generics.CreateAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = (IsAuthenticated,)


class AttachmentDestroy(generics.DestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (IsIssueOwner,)


class AttachmentListForIssue(generics.ListAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Attachment.objects.filter(issue_id=self.kwargs['issue_id'])
