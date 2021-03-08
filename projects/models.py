from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(max_length=256, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='projects_owning')
    creation_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(get_user_model(), related_name='projects')

    def __str__(self):
        return self.name


class Issue(models.Model):
    TODO = 'TODO'
    IN_PROGRESS = 'IP'
    REVIEW = 'REV'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (TODO, 'Todo'),
        (IN_PROGRESS, 'In progress'),
        (REVIEW, 'Review'),
        (DONE, 'Done'),
    )

    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='issues_owning')
    assignee = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='issues')
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default=TODO)

    def __str__(self):
        return self.title
