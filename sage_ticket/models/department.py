from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TimeStampMixin


class Department(TimeStampMixin):
    """Model to represent a department within an organization."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("The title of the department."),
        db_comment="The title of the department.",
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("A description of the department."),
        db_comment="A description of the department.",
    )
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="users",
        verbose_name=_("Members"),
        help_text=_("The members of the department."),
        db_comment="The members of the department.",
    )

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        db_table = "sage_ticket_department"

    def __repr__(self):
        return f"<Department(id={self.id}, title={self.title})>"

    def __str__(self) -> str:
        return self.title
