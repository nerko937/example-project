from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ('head', 'get', 'post', 'put', 'patch')

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

