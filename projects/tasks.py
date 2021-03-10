from example_project.celery import app
from .models import Issue
from .utils import email_due_date_passed


@app.task
def email_when_due_date_passed(issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        pass

    if issue.status != issue.DONE:
        email_due_date_passed(issue)
