from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('head', 'get', 'post', 'put', 'patch')

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)
