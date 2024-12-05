from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TimeStampMixin

from sage_ticket.helper import ExtensionsEnum


class Attachment(TimeStampMixin):
    """Model to represent attachments related to issues."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("The name of the attachment."),
        db_comment="The name of the attachment.",
    )
    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Issue"),
        help_text=_("The issue to which this attachment is related."),
        db_comment="The issue to which this attachment is related.",
    )
    extensions = models.CharField(
        choices=ExtensionsEnum.choices,
        max_length=20,
        verbose_name=_("Extension"),
        help_text=_("The file extension of the attachment."),
        db_comment="The file extension of the attachment.",
    )
    file = models.FileField(
        _("Issue file"),
        upload_to="media/uploads",
        help_text=_("The file that is uploaded."),
        db_comment="The file that is uploaded.",
    )

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        db_table = "sage_ticket_attachment"

    def __repr__(self):
        return f"<Attachment(id={self.id}, name={self.name}"

    def __str__(self) -> str:
        return self.name
