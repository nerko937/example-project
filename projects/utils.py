from bleach import Cleaner
from bleach.linkifier import LinkifyFilter
from django.conf import settings
from django.core.mail import send_mail
import markdown


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


def issue_directory_path(instance, filename):
    """for FileField upload_to"""
    return f'attachments/issue_{instance.issue_id}/{filename}'


def md_to_html(md):
    """Converts md to html and sanitizes it"""
    html = markdown.markdown(md)
    cleaner = Cleaner(
        tags=[
            "h1", "h2", "h3", "h4", "h5", "h6",
            "b", "i", "strong", "em", "tt", "del", "abbr",
            "p", "br",
            "span", "div", "blockquote", "code", "pre", "hr",
            "ul", "dl", "ol", "li", "dd", "dt",
            "img",
            "a",
            "sub", "sup",
        ],
        attributes={
            "img": ["src", "alt", "title"],
            "a": ["href", "alt", "title"],
            "abbr": ["title"],
        },
        filters=[LinkifyFilter],
    )
    return cleaner.clean(html)
