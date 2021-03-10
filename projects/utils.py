from django.core.mail import send_mail
from django.conf import settings


def email_due_date_passed(issue):
    send_mail(
        "One of issues due date passed and it's not completed",
        f"Issue {issue.title} passed due date and it's not completed yet.",
        settings.MAIL_INFO,
        [issue.owner, issue.assignee],
        fail_silently=False,
    )


def email_if_assignee_changed(issue):
    if issue.tracker.has_changed('assignee'):
        send_mail(
            "Information about issue assignee change",
            "Issue {} has new assignee. Changed from {} to {}.".format(
                issue.title,
                issue.tracker.previous('assignee'),
                issue.assignee,
            ),
            settings.MAIL_INFO,
            [issue.owner, issue.assignee],
            fail_silently=False,
        )
