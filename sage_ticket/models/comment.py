from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TimeStampMixin

from sage_ticket.helper import StatusEnum


class Comment(TimeStampMixin):
    """Model to represent comments related to issues."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("The title of the comment."),
        db_comment="The title of the comment.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="comments",
        help_text=_("The user who made the comment."),
        db_comment="The user who made the comment.",
    )
    issue = models.ForeignKey(
        "Issue",
        verbose_name=_("Issue"),
        on_delete=models.CASCADE,
        related_name="comments",
        help_text=_("The issue to which this comment is related."),
        db_comment="The issue to which this comment is related.",
    )
    message = models.TextField(
        max_length=255,
        verbose_name=_("Message"),
        help_text=_("The content of the comment."),
        db_comment="The content of the comment.",
    )
    is_read = models.BooleanField(
        verbose_name=_("Is Read"),
        help_text=_("Indicates if the comment is unread."),
        db_comment="Indicates if the comment is unread.",
    )
    status = models.CharField(
        choices=StatusEnum.choices,
        max_length=10,
        verbose_name=_("Status"),
        help_text=_("The status of the comment."),
        db_comment="The status of the comment.",
    )
    replay = models.ForeignKey(
        "self",
        verbose_name=_("Replay"),
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        help_text=_("The comment to which this is a reply."),
        db_comment="The comment to which this is a reply.",
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        db_table = "sage_ticket_comment"

    def __repr__(self):
        return f"<Comment(id={self.id}, title={self.title},user={self.user_id}"

    def __str__(self) -> str:
        return self.title
