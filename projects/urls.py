from django.urls import path
from rest_framework import routers

from .views import (
    ProjectViewSet,
    IssueCreate,
    IssueRetrieveUpdate,
    IssueListForProject,
    AttachmentCreate,
    AttachmentDestroy,
    AttachmentListForIssue,
)


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
urlpatterns = [
    path('projects/<int:project_id>/issues/', IssueListForProject.as_view()),
    path('issues/', IssueCreate.as_view()),
    path('issues/<int:pk>/', IssueRetrieveUpdate.as_view()),
    path('issues/<int:issue_id>/attachments/', AttachmentListForIssue.as_view()),
    path('attachments/', AttachmentCreate.as_view()),
    path('attachments/<int:pk>/', AttachmentDestroy.as_view()),
] + router.urls
