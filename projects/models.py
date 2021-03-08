from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(max_length=256, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='project_owning')
    creation_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(get_user_model(), related_name='projects')

    def __str__(self):
        return self.name
