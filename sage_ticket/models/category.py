from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin

from sage_ticket.repository.manager import CategoryDataAccessLayer


class TutorialCategory(TitleSlugMixin, TimeStampMixin):
    """
    Tutorial Category
    """

    is_published = models.BooleanField(
        _("Is Published"),
        default=True,
        help_text=_(
            "Indicate whether this category is currently published and should be "
            "displayed to all users. If unpublished, only staff users can view "
            "the category."
        ),
        db_comment=(
            "Indicates if the category is published (true) or hidden from "
            "non-staff users (false)."
        ),
    )

    objects: CategoryDataAccessLayer = CategoryDataAccessLayer()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        default_manager_name = "objects"
        db_table = "sage_tutorial_category"
        db_table_comment = "Table for categorizing blog tutorials"

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"<Tutorial Category: {self.title}>"
