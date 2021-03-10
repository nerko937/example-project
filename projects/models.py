from django.db import models
from django.contrib.auth import get_user_model
from model_utils import FieldTracker

from example_project.celery import app
from .utils import email_if_assignee_changed


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
    task_id = models.UUIDField(null=True, blank=True)
    tracker = FieldTracker(fields=['due_date', 'assignee'])

    def __str__(self):
        return self.title

    def notify_when_due_date_passed(self):
        from .tasks import email_when_due_date_passed

        t = email_when_due_date_passed.apply_async((self.pk,), eta=self.due_date)
        self.task_id = t.task_id
        self.save(update_fields=['task_id'])

    def save(self, *args, **kwargs):
        is_new = not self.pk
        due_date_changed = self.tracker.has_changed('due_date')
        email_if_assignee_changed(self)
        super().save(*args, **kwargs)
        if is_new:
            self.notify_when_due_date_passed()
        elif due_date_changed:
            app.control.revoke(self.task_id, terminate=True)
            self.notify_when_due_date_passed()
